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
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/pulumi/pulumi/pkg/v3/testing/integration"
	ptesting "github.com/pulumi/pulumi/sdk/v3/go/common/testing"
)

// TestPulumiDockerImage simulates building and running Pulumi programs on the pulumi/pulumi Docker image.
//
// NOTE: This test is intended to be run inside the aforementioned container, unlike the actions test below.
func TestPulumiDockerImage(t *testing.T) {
	if os.Getenv("RUN_CONTAINER_TESTS") == "" {
		t.Skip("Skipping container runtime tests because RUN_CONTAINER_TESTS not set.")
	}

	// Confirm we have credentials.
	if os.Getenv("PULUMI_ACCESS_TOKEN") == "" {
		t.Fatal("PULUMI_ACCESS_TOKEN not found, aborting tests.")
	}

	stackOwner := os.Getenv("PULUMI_ORG")
	if stackOwner == "" {
		t.Fatal("PULUMI_ORG must be set.  Aborting tests.")
	}

	sdksToTest := []string{"csharp", "python", "typescript", "go", "java"}
	if os.Getenv("SDKS_TO_TEST") != "" {
		sdksToTest = strings.Split(os.Getenv("SDKS_TO_TEST"), ",")
	}

	base := integration.ProgramTestOptions{
		Tracing:              "https://tracing.pulumi-engineering.com/collector/api/v1/spans",
		ExpectRefreshChanges: true,
		Quick:                true,
		SkipRefresh:          true,
		NoParallel:           true, // we mark tests as Parallel manually when instantiating
	}

	for _, template := range sdksToTest {
		t.Run(template, func(t *testing.T) {
			t.Parallel()

			e := ptesting.NewEnvironment(t)
			defer func() {
				e.RunCommand("pulumi", "stack", "rm", "--force", "--yes")
				e.DeleteEnvironment()
			}()

			stackName := fmt.Sprintf("%s/container-%s-%x", stackOwner, template, time.Now().UnixNano())
			e.RunCommand("pulumi", "new", template, "-y", "-f", "-s", stackName)

			example := base.With(integration.ProgramTestOptions{
				Dir: e.RootPath,
			})

			integration.ProgramTest(t, &example)
		})
	}

	t.Run("python venv", func(t *testing.T) {
		t.Parallel()

		e := ptesting.NewEnvironment(t)
		defer func() {
			e.DeleteEnvironment()
		}()

		e.RunCommand("python3", "-m", "venv", filepath.Join(e.RootPath, "venv"))
	})
}
