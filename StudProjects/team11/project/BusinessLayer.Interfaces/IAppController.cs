using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Model;
namespace BusinessLayer.Interfaces
{
    public interface IAppController
    {
        List<App> GetAllApplications();
        void AddApp(App app);
        Process StartApp(App app);
        void RemoveApp(App app);
    }
}
