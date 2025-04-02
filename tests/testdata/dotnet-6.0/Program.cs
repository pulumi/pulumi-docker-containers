using System.Collections.Generic;
using Pulumi;

return await Deployment.RunAsync(() =>
{
    var version = System.Environment.Version;
    // TargetFramework is 6.0, but we will be running on a later version.
    if (version.Major ==  6) {
        throw new System.Exception("Expected .NET different from 6.0, but got, " + version.Major);
    }
});
