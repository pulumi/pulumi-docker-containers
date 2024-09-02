using System.Collections.Generic;
using Pulumi;

return await Deployment.RunAsync(() =>
{
    var version = System.Environment.Version;
    if (version.Major != 6) {
        throw new System.Exception("Expected .NET 6 runtime, got " + version.Major);
    }
});
