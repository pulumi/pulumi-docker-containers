using System.Collections.Generic;
using Pulumi;

return await Deployment.RunAsync(() =>
{
    var version = System.Environment.Version;
    if (version.Major != 10)
    {
        throw new System.Exception("Expected .NET 10 runtime, got " + version.Major);
    }
});
