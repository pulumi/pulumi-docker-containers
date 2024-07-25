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
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"strings"
	"testing"
	"time"

	"github.com/pulumi/pulumi/pkg/v3/testing/integration"
	ptesting "github.com/pulumi/pulumi/sdk/v3/go/common/testing"
	"github.com/stretchr/testify/require"
)

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

	stackOwner := mustEnv(t, "PULUMI_ORG")

	sdksToTest := []string{"csharp", "python", "typescript", "go", "java"}
	if os.Getenv("SDKS_TO_TEST") != "" {
		sdksToTest = strings.Split(os.Getenv("SDKS_TO_TEST"), ",")
	}
	clouds := []string{"azure", "aws" /* , "gcp"*/}
	configs := map[string]map[string]string{
		"azure": {
			"azure-native:location": "EastUS",
		},
		"aws": {},
	}

	testCases := []testCase{}
	for _, sdk := range sdksToTest {
		// python, typescript, ...
		testCases = append(testCases, testCase{sdk, map[string]string{}})
		for _, cloud := range clouds {
			// azure-python, aws-python, ...
			if sdk == "typescript" && cloud == "azure" {
				// We use docker & qemu to run arm64 images, and azure seems to be too large
				// to successfully run in that environment.
				// TODO: https://github.com/pulumi/pulumi-docker-containers/issues/211
				continue
			}
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
			// TODO: Not running these in parallel to help with disk space.
			// https://github.com/pulumi/pulumi-docker-containers/issues/215
			// t.Parallel()
			e := ptesting.NewEnvironment(t)
			defer func() {
				e.RunCommand("pulumi", "stack", "rm", "--force", "--yes")
				e.DeleteEnvironment()
			}()

			stackName := fmt.Sprintf("%s/container-%s-%x", stackOwner, test.template, time.Now().UnixNano())
			e.RunCommand("pulumi", "new", test.template, "-y", "-f", "-s", stackName)

			example := base.With(integration.ProgramTestOptions{
				Dir:    e.RootPath,
				Config: test.config,
			})

			integration.ProgramTest(t, &example)
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
	})
}

func mustEnv(t *testing.T, env string) string {
	t.Helper()
	v := os.Getenv(env)
	if v == "" {
		t.Fatalf("Required environment variable %q not set", env)
	}
	return v
}
