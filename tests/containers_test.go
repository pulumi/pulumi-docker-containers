// Copyright 2021-2024, Pulumi Corporation.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package containers

import (
	"crypto/rand"
	"embed"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/pulumi/pulumi/pkg/v3/engine"
	"github.com/pulumi/pulumi/pkg/v3/testing/integration"
	ptesting "github.com/pulumi/pulumi/sdk/v3/go/common/testing"
	"github.com/stretchr/testify/require"
)

//go:embed all:testdata
var testdata embed.FS

type testCase struct {
	template string
	config   map[string]string
}

// TestPulumiTemplateTests simulates building and running Pulumi programs on the pulumi/pulumi Docker image.
//
// NOTE: This test is intended to be run inside the aforementioned container.
func TestPulumiTemplateTests(t *testing.T) {
	t.Parallel()

	// Confirm we have credentials.
	// Azure
	mustEnv(t, "PULUMI_ACCESS_TOKEN")
	mustEnv(t, "ARM_CLIENT_ID")
	mustEnv(t, "ARM_CLIENT_SECRET")
	mustEnv(t, "ARM_TENANT_ID")
	// AWS
	mustEnv(t, "AWS_ACCESS_KEY_ID")
	mustEnv(t, "AWS_SECRET_ACCESS_KEY")
	mustEnv(t, "AWS_SESSION_TOKEN")
	// GCP
	project := mustEnv(t, "GCP_PROJECT_NAME")
	mustEnv(t, "GOOGLE_APPLICATION_CREDENTIALS")

	stackOwner := mustEnv(t, "PULUMI_ORG")

	languageVersion := os.Getenv("LANGUAGE_VERSION") // Not set for kitchen sink

	sdksToTest := []string{"csharp", "python", "typescript", "go", "java"}
	if os.Getenv("SDKS_TO_TEST") != "" {
		sdksToTest = strings.Split(os.Getenv("SDKS_TO_TEST"), ",")
	}
	clouds := []string{"gcp", "azure", "aws"}
	configs := map[string]map[string]string{
		"azure": {
			"azure-native:location": "EastUS",
		},
		"aws": {},
		"gcp": {
			"gcp:project": project,
		},
	}

	testCases := []testCase{}
	for _, sdk := range sdksToTest {
		if sdk == "csharp" && languageVersion == "6.0" {
			// .NET 6.0 is not supported by our templates anymore.
			continue
		}
		// Base language templates: python, typescript, ...
		testCases = append(testCases, testCase{sdk, map[string]string{}})
		for _, cloud := range clouds {
			// Cloud templates azure-python, aws-python, ...
			testCases = append(testCases, testCase{
				template: fmt.Sprintf("%s-%s", cloud, sdk),
				config:   configs[cloud],
			})
		}
	}

	base := integration.ProgramTestOptions{
		ExpectRefreshChanges: true,
		Quick:                true,
		SkipRefresh:          true,
		NoParallel:           true, // we mark tests as Parallel manually when instantiating
	}

	for _, test := range testCases {
		test := test
		t.Run(test.template, func(t *testing.T) {
			t.Parallel()

			e := ptesting.NewEnvironment(t)
			defer func() {
				e.RunCommand("pulumi", "stack", "rm", "--force", "--yes")
				e.DeleteEnvironment()
			}()

			stackName := fmt.Sprintf("%s/container-%s-%x", stackOwner, test.template, time.Now().UnixNano())
			e.RunCommand("pulumi", "new", test.template, "-y", "-f", "-s", stackName)

			example := base.With(integration.ProgramTestOptions{
				Dir:        e.RootPath,
				Config:     test.config,
				NoParallel: true, // Called above
				// `pulumi new` already runs `pulumi install for us, don't attempt to `yarn link`
				// the SDK into the test.
				PrepareProject: func(info *engine.Projinfo) error {
					return nil
				},
			})

			integration.ProgramTest(t, &example)
		})
	}
}

func TestKitchenSinkLanguageVersions(t *testing.T) {
	if !isKitchenSink(t) {
		t.Skip("Only language version tests on kitchen sink")
	}
	t.Parallel()

	dirs, err := testdata.ReadDir("testdata")
	require.NoError(t, err)

	t.Run("node-default", func(t *testing.T) {
		// We need to run the `node-default` test first, before the other tests which modify
		// the container's default node version.
		p := filepath.Join("testdata", "node-default")
		copyTestData(t, p)
		integration.ProgramTest(t, &integration.ProgramTestOptions{
			NoParallel:  true,
			Dir:         p,
			Quick:       true,
			SkipRefresh: true,
			PrepareProject: func(info *engine.Projinfo) error {
				cmd := exec.Command("pulumi", "install", "--use-language-version-tools")
				cmd.Dir = info.Root
				out, err := cmd.CombinedOutput()
				if err != nil {
					t.Logf("install failed: %s: %s", err, out)
				}
				return err
			},
		})
	})

	for _, dir := range dirs {
		dir := dir
		t.Run(dir.Name(), func(t *testing.T) {
			if dir.Name() == "node-default" {
				// The `node-default` test is run first, so we skip it here.
				t.Skip()
			}
			p := filepath.Join("testdata", dir.Name())
			copyTestData(t, p)
			integration.ProgramTest(t, &integration.ProgramTestOptions{
				// We can't run the node tests in parallel because setting the node version is a
				// global for the container.
				NoParallel:  strings.HasPrefix(dir.Name(), "node-"),
				Dir:         p,
				Quick:       true,
				SkipRefresh: true,
				PrepareProject: func(info *engine.Projinfo) error {
					cmd := exec.Command("pulumi", "install", "--use-language-version-tools")
					cmd.Dir = info.Root
					out, err := cmd.CombinedOutput()
					if err != nil {
						t.Logf("install failed: %s: %s", err, out)
					}
					return err
				},
			})
		})
	}
}

func TestCLIToolTests(t *testing.T) {
	t.Parallel()

	t.Run("Azure CLI", func(t *testing.T) {
		t.Parallel()

		clientId := mustEnv(t, "ARM_CLIENT_ID")
		clientSecret := mustEnv(t, "ARM_CLIENT_SECRET")
		tenantId := mustEnv(t, "ARM_TENANT_ID")
		subscriptionId := mustEnv(t, "ARM_SUBSCRIPTION_ID")

		cmd := exec.Command("az", "login", "--service-principal",
			"--username", clientId,
			"--password", clientSecret,
			"--tenant", tenantId)
		_, err := cmd.Output()
		require.NoError(t, err)

		cmd = exec.Command("az", "account", "show")
		out, err := cmd.Output()
		require.NoError(t, err)
		result := map[string]interface{}{}
		require.NoError(t, json.Unmarshal(out, &result))
		require.Equal(t, subscriptionId, result["id"])
	})

	t.Run("AWS CLI", func(t *testing.T) {
		t.Parallel()

		mustEnv(t, "AWS_ACCESS_KEY_ID")
		mustEnv(t, "AWS_SECRET_ACCESS_KEY")
		mustEnv(t, "AWS_SESSION_TOKEN")
		mustEnv(t, "AWS_REGION")

		cmd := exec.Command("aws", "sts", "get-caller-identity")
		out, err := cmd.Output()
		require.NoError(t, err)
		result := map[string]interface{}{}
		require.NoError(t, json.Unmarshal(out, &result))
		arn, ok := result["Arn"].(string)
		require.True(t, ok)
		require.Contains(t, arn, "pulumi-docker-containers@githubActions")

		// Ensure that aws-iam-authenticator is installed
		cmd = exec.Command("aws-iam-authenticator", "token", "--cluster-id", "test-123")
		out, err = cmd.Output()
		require.NoError(t, err)
		require.Contains(t, string(out), "ExecCredential")
	})

	t.Run("GCP CLI", func(t *testing.T) {
		t.Parallel()

		project := mustEnv(t, "GCP_PROJECT_NAME")
		projectNumber := mustEnv(t, "GCP_PROJECT_NUMBER")
		credsFile := mustEnv(t, "GOOGLE_APPLICATION_CREDENTIALS")

		cmd := exec.Command("gcloud", "--quiet", "auth", "login", "--force", "--cred-file", credsFile)
		out, err := cmd.CombinedOutput()
		require.NoError(t, err)

		cmd = exec.Command("gcloud", "--quiet", "config", "set", "project", project)
		out, err = cmd.CombinedOutput()
		require.NoError(t, err)

		cmd = exec.Command("gcloud", "--quiet", "projects", "describe", project, "--format", "json")
		out, err = cmd.CombinedOutput()
		require.NoError(t, err)
		var projectInfo map[string]interface{}
		require.NoError(t, json.Unmarshal(out, &projectInfo))
		projectNumber, ok := projectInfo["projectId"].(string)
		if !ok {
			require.Failf(t, "projectId not found in %s", string(out))
		}
		require.Equal(t, project, projectNumber)
	})
}

func TestEnvironment(t *testing.T) {
	t.Parallel()
	// Deployment steps are run via bash, and explicitly set BASH_ENV to source ~/.bashrc.
	// https://github.com/pulumi/pulumi-service/blob/8cbd9397ec0cdc7b5c168715ca4c9aa087c83823/cmd/workflow-runner/run.go#L78
	// We run commands that check basic assertions about the environment within the container once
	// directly without shell and once with bash to ensure that the environment is set up correctly
	// for both cases.
	// This is a regression test for https://github.com/pulumi/pulumi-docker-containers/issues/193

	imageVariant := os.Getenv("IMAGE_VARIANT")
	t.Logf("Testing image variant: %s", imageVariant)

	t.Run("Python", func(t *testing.T) {
		if !hasPython(t) {
			t.Skip("Skipping test for images without python")
		}
		t.Parallel()
		expected := "/usr/local/bin/python"
		if isKitchenSink(t) || isUBI(t) {
			expected = "/usr/local/share/pyenv/shims/python"
		}
		p, err := exec.LookPath("python")
		require.NoError(t, err)
		require.Equal(t, expected, p)
		// Use bash `command` builtin to lookup the path to python
		requireOutputWithBash(t, expected, "command", "-v", "python")

		// Poetry should be available
		expectedPoetryPath := "/usr/local/bin/poetry"
		poetryPath, err := exec.LookPath("poetry")
		require.NoError(t, err)
		require.Equal(t, expectedPoetryPath, poetryPath)
		// Use bash `command` builtin to lookup the path to poetry
		requireOutputWithBash(t, expectedPoetryPath, "command", "-v", "poetry")

		// uv should be available
		expectedUvPath := "/usr/local/bin/uv"
		uvPath, err := exec.LookPath("uv")
		require.NoError(t, err)
		require.Equal(t, expectedUvPath, uvPath)
		// Use bash `command` builtin to lookup the path to uv
		requireOutputWithBash(t, expectedUvPath, "command", "-v", "uv")
	})

	t.Run("Node", func(t *testing.T) {
		if !hasNodejs(t) {
			t.Skip("Skipping test for images without nodejs")
		}
		t.Parallel()

		for _, testCase := range []struct {
			name            string
			expectedDebian  string
			expectedUbi     string
			expectedKitchen string
		}{
			{
				name:            "node",
				expectedDebian:  "/usr/local/bin/node",
				expectedUbi:     "/usr/local/share/fnm/aliases/default/bin/node",
				expectedKitchen: "/usr/local/share/fnm/aliases/default/bin/node",
			},
			{
				name:            "npm",
				expectedDebian:  "/usr/local/bin/npm",
				expectedUbi:     "/usr/local/share/fnm/aliases/default/bin/npm",
				expectedKitchen: "/usr/local/share/fnm/aliases/default/bin/npm",
			},
			{
				name:            "yarn",
				expectedDebian:  "/usr/local/bin/yarn",
				expectedUbi:     "/usr/local/share/fnm/aliases/default/bin/yarn",
				expectedKitchen: "/usr/local/share/fnm/aliases/default/bin/yarn",
			},
			{
				name:            "corepack",
				expectedDebian:  "/usr/local/bin/corepack",
				expectedUbi:     "/usr/local/share/fnm/aliases/default/bin/corepack",
				expectedKitchen: "/usr/local/share/fnm/aliases/default/bin/corepack",
			},
			{
				name:            "bun",
				expectedDebian:  "/usr/local/bin/bun",
				expectedUbi:     "/usr/local/share/fnm/aliases/default/bin/bun",
				expectedKitchen: "/usr/local/share/fnm/aliases/default/bin/bun",
			},
			{
				name:            "pnpm",
				expectedDebian:  "/usr/local/bin/pnpm",
				expectedUbi:     "/usr/local/share/fnm/aliases/default/bin/pnpm",
				expectedKitchen: "/usr/local/share/fnm/aliases/default/bin/pnpm",
			},
		} {
			testCase := testCase
			t.Run(testCase.name, func(t *testing.T) {
				t.Parallel()
				expected := testCase.expectedDebian
				if isUBI(t) {
					expected = testCase.expectedUbi
				}
				if isKitchenSink(t) {
					expected = testCase.expectedKitchen
				}
				p, err := exec.LookPath(testCase.name)
				require.NoError(t, err)
				require.Equal(t, expected, p)
				// Use bash `command` builtin to lookup the path when running in bash
				requireOutputWithBash(t, expected, "command", "-v", testCase.name)
			})
		}
	})

	t.Run(imageVariant, func(t *testing.T) {
		t.Parallel()
		// Install scripts for various tools can sometimes modify PATH, usually by adding entries
		// to ~/.bashrc. This test ensures that we notice such modifications.
		expectedPaths := map[string]string{
			"pulumi":               "/pulumi/bin:/usr/local/share/fnm/aliases/default/bin:/usr/local/share/pyenv/shims:/usr/local/share/pyenv/bin:/usr/local/share/dotnet:/go/bin:/usr/local/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
			"pulumi-nonroot":       "/pulumi/bin:/usr/local/share/fnm/aliases/default/bin:/usr/local/share/pyenv/shims:/usr/local/share/pyenv/bin:/usr/local/share/dotnet:/go/bin:/usr/local/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
			"pulumi-debian-dotnet": "/root/.dotnet:/pulumi/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
			"pulumi-debian-go":     "/pulumi/bin:/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
			"pulumi-debian-java":   "/pulumi/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
			"pulumi-debian-nodejs": "/pulumi/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
			"pulumi-debian-python": "/pulumi/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
			"pulumi-ubi-dotnet":    "/root/.dotnet:/pulumi/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
			"pulumi-ubi-go":        "/pulumi/bin:/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
			"pulumi-ubi-java":      "/pulumi/bin:/root/.sdkman/candidates/maven/current/bin:/root/.sdkman/candidates/gradle/current/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
			"pulumi-ubi-nodejs":    "/pulumi/bin:/usr/local/share/fnm/aliases/default/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
			"pulumi-ubi-python":    "/pulumi/bin:/usr/local/share/pyenv/shims:/usr/local/share/pyenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
		}

		t.Run("PATH when running in bash", func(t *testing.T) {
			t.Parallel()
			expectedPath := expectedPaths[imageVariant]
			// When running in bash, we pick up the PATH entry from the pulumi installation script.
			if imageVariant == "pulumi" {
				expectedPath += ":/root/.pulumi/bin"
			}
			// When running in bash, the UBI images include /root/.local/bin:/root/bin:
			if isUBI(t) {
				expectedPath = "/root/.local/bin:/root/bin:" + expectedPath
			}
			requireOutputWithBash(t, expectedPath, "printenv", "PATH")
		})

		t.Run("PATH without any shell", func(t *testing.T) {
			t.Parallel()
			expectedPath := expectedPaths[imageVariant]
			requireOutput(t, expectedPath, "printenv", "PATH")
		})
	})

	// All images must include curl. Deployments uses this to download the executor binary.
	t.Run("Curl", func(t *testing.T) {
		t.Parallel()

		cmd := exec.Command("curl", "--version")
		_, err := cmd.Output()
		require.NoError(t, err)
	})

	// All images must include git. Deployments uses this to checkout the source code.
	t.Run("Git", func(t *testing.T) {
		t.Parallel()

		cmd := exec.Command("git", "--version")
		err := cmd.Run()
		require.NoError(t, err)
	})

	// We only support yarn classic
	t.Run("Yarn", func(t *testing.T) {
		if !hasNodejs(t) {
			t.Skip("Skipping test for images without nodejs")
		}
		t.Parallel()

		cmd := exec.Command("yarn", "--version")
		out, err := cmd.CombinedOutput()
		require.NoError(t, err)
		require.True(t, strings.HasPrefix(string(out), "1."))
	})

	t.Run("Workdir", func(t *testing.T) {
		t.Parallel()
		// Kitchen sink does not set `WORKDIR`.
		if imageVariant == "pulumi" || imageVariant == "pulumi-nonroot" {
			requireOutput(t, "/", "pwd")
			requireOutputWithBash(t, "/", "pwd")
		} else {
			requireOutput(t, "/pulumi/projects", "pwd")
			requireOutputWithBash(t, "/pulumi/projects", "pwd")
		}
	})

	t.Run("User", func(t *testing.T) {
		t.Parallel()
		if isNonRoot(t) {
			requireOutput(t, "pulumi", "whoami")
			requireOutputWithBash(t, "pulumi", "whoami")
		} else {
			requireOutput(t, "root", "whoami")
			requireOutputWithBash(t, "root", "whoami")
		}
	})

	t.Run("Home", func(t *testing.T) {
		t.Parallel()
		if isNonRoot(t) {
			requireOutput(t, "/home/pulumi", "printenv", "HOME")
			requireOutputWithBash(t, "/home/pulumi", "printenv", "HOME")
		} else {
			requireOutput(t, "/root", "printenv", "HOME")
			requireOutputWithBash(t, "/root", "printenv", "HOME")
		}
	})
}

func requireOutput(t *testing.T, expected, cmd string, args ...string) {
	c := exec.Command(cmd, args...)
	t.Logf("Running %q", c.String())
	out, err := c.Output()
	require.NoError(t, err)
	o := strings.TrimSpace(string(out))
	require.Equal(t, expected, o)
}

func requireOutputWithBash(t *testing.T, expected, cmd string, args ...string) {
	bashArgs := strings.Join(append([]string{cmd}, args...), " ")
	c := exec.Command("/bin/bash", "-c", bashArgs)
	c.Env = append(os.Environ(), "BASH_ENV=/root/.bashrc")
	t.Logf("Running %q", c.String())
	out, err := c.Output()
	require.NoError(t, err)
	o := strings.TrimSpace(string(out))
	require.Equal(t, expected, o)
}

func mustEnv(t *testing.T, env string) string {
	t.Helper()
	v := os.Getenv(env)
	if v == "" {
		t.Fatalf("Required environment variable %q not set", env)
	}
	return v
}

func isKitchenSink(t *testing.T) bool {
	imageVariant := mustEnv(t, "IMAGE_VARIANT")
	return imageVariant == "pulumi"
}

func hasPython(t *testing.T) bool {
	imageVariant := mustEnv(t, "IMAGE_VARIANT")
	return strings.HasSuffix(imageVariant, "python") || isKitchenSink(t)
}

func hasNodejs(t *testing.T) bool {
	imageVariant := mustEnv(t, "IMAGE_VARIANT")
	return strings.HasSuffix(imageVariant, "nodejs") || isKitchenSink(t)
}

func isDebian(t *testing.T) bool {
	imageVariant := mustEnv(t, "IMAGE_VARIANT")
	return strings.HasPrefix(imageVariant, "pulumi-debian")
}

func isUBI(t *testing.T) bool {
	imageVariant := mustEnv(t, "IMAGE_VARIANT")
	return strings.HasPrefix(imageVariant, "pulumi-ubi")
}

func isNonRoot(t *testing.T) bool {
	imageVariant := mustEnv(t, "IMAGE_VARIANT")
	return strings.HasSuffix(imageVariant, "-nonroot")
}

func RandomStackName(t *testing.T) string {
	t.Helper()
	b := make([]byte, 4)
	_, err := rand.Read(b)
	require.NoError(t, err)
	return "test" + hex.EncodeToString(b)
}

func copyTestData(t *testing.T, path string) {
	require.NoError(t, os.MkdirAll(path, os.ModePerm))
	files, err := testdata.ReadDir(path)
	require.NoError(t, err, "readdir")
	for _, file := range files {
		p := filepath.Join(path, file.Name())
		fileContent, err := testdata.ReadFile(p)
		require.NoError(t, err, "readfile")
		require.NoError(t, os.WriteFile(p, fileContent, os.ModePerm), "writefile")
	}
}
