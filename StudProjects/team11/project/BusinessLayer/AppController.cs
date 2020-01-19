using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using BusinessLayer.Interfaces;
using DataLayer;
using Model;

namespace BusinessLayer
{
    public class AppController : IAppController
    {
        public void AddApp(App app)
        {
            using (ApplicationDbContext applicationDbContext = new ApplicationDbContext())
            {
                applicationDbContext.Apps.Add(app);
                applicationDbContext.SaveChanges();
            }
        }

        public List<App> GetAllApplications()
        {
            using (ApplicationDbContext applicationDbContext = new ApplicationDbContext())
            {
                return applicationDbContext.Apps.ToList();
            }
        }

        public void RemoveApp(App app)
        {
            using (ApplicationDbContext applicationDbContext = new ApplicationDbContext())
            {
                applicationDbContext.Apps.Remove(app);
                applicationDbContext.SaveChanges();
            }
        }

        public Process StartApp(App app)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = app.Path;
            start.WindowStyle = ProcessWindowStyle.Hidden;

            // Run the external process & wait for it to finish
            Process process = new Process();
            process.StartInfo = start;
            process.EnableRaisingEvents = true;
            process.Start();

            return process;
        }
    }
}
