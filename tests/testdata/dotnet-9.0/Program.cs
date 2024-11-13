using System.Collections.Generic;
using Pulumi;

return await Deployment.RunAsync(() =>
{
    var version = System.Environment.Version;
    if (version.Major != 9)
    {
        throw new System.Exception("Expected .NET 9 runtime, got " + version.Major);
    }
});
