using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace MedHelp.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public ActionResult Index(HttpPostedFileBase file)
        {

            if (file.ContentLength > 0)
            {
                var fileName = Path.GetFileName(file.FileName);
                var path = Path.Combine(Server.MapPath("~/Commands/Algorithm/testing"), "testing_axial_full_pat10.nii.gz");
                file.SaveAs(path);
                return ExecuteSegmentation(fileName);
            }
            return RedirectToAction("Index");
        }

        private FileContentResult ExecuteSegmentation(string fileName)
        {
            var processInfo = new ProcessStartInfo("cmd.exe", @"/c D:\ITSGFork\StudProjects\team00\WebApp\MedHelp\Commands\HeartMri.bat")
            {
                CreateNoWindow = true,
                UseShellExecute = false
            };

            var process = Process.Start(processInfo);

            process.Start();

            process.WaitForExit();
            if (process.HasExited)
            {
                process.Close();
                String file = Server.MapPath("~/Commands/Algorithm/models/testing/" + "window_seg_pat10__segmentation_niftynet.nii.gz");
                String mimeType = MimeMapping.GetMimeMapping(file);

                byte[] stream = System.IO.File.ReadAllBytes(file);
                return File(stream, mimeType);
            }
            return null;
        }


    }
}