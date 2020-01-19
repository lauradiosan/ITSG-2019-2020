using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BusinessLayer
{
    public class ImageController
    {
        private static string path;
        public ImageController()
        {
            path = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "Children");
        }

        public string SaveImage(Bitmap image)
        {
            Guid guid = Guid.NewGuid();
            string imagePath = Path.Combine(path, guid.ToString());
            image.Save(imagePath);
            return imagePath;
        }
    }
}
