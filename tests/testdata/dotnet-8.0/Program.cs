using System.Collections.Generic;
using Pulumi;

return await Deployment.RunAsync(() =>
{
    var version = System.Environment.Version;
    if (version.Major != 8) {
        throw new System.Exception("Expected .NET 8 runtime, got " + version.Major);
    }
});
