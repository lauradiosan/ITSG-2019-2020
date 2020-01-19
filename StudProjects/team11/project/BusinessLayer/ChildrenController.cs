using BusinessLayer.Interfaces;
using DataLayer;
using Model;
using Services;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;

namespace BusinessLayer
{
    public class ChildrenController : IChildrenController
    {
        private ConcurrentDictionary<int, Child> children;
        private static string path;

        public ChildrenController()
        {
            this.children = new ConcurrentDictionary<int, Child>(this.GetAllChildren().ToDictionary(child => child.Id, child => child));
            path = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "Children");
            Directory.CreateDirectory(path);
        }

        public void AddChild(Child child, Bitmap image)
        {
            var savePath = this.SaveImage(image);
            child.ImageId = savePath;
            using (ApplicationDbContext applicationDbContext = new ApplicationDbContext())
            {
                applicationDbContext.Children.Add(child);
                applicationDbContext.SaveChanges();
            }

            this.children.TryAdd(child.Id, child);
        }

        public List<Child> GetAllChildren()
        {
            using (ApplicationDbContext applicationDbContext = new ApplicationDbContext())
            {
                return applicationDbContext.Children.ToList();
            }
        }

        public void RemoveChild(int id)
        {
            Child child;
            using (ApplicationDbContext applicationDbContext = new ApplicationDbContext())
            {
                child = applicationDbContext.Children.Find(id);
                applicationDbContext.Children.Remove(child);
                applicationDbContext.SaveChanges();
            }

            this.children.TryRemove(child.Id, out Child a);
            this.RemoveImage(child.ImageId);
        }

        public Child GetChildByYhat(double[] yhat)
        {
            (Child child, double similarity) bestMatch = this.children.AsParallel()
                .Select(u => (u.Value, this.GetCosineSimilarity(u.Value.Yhat, yhat)))
                .Aggregate((new Child(), 0.0), (i1, i2) => i1.Item2 > i2.Item2 ? i1 : i2);

            if (bestMatch.similarity < 0.7)
            {
                return null;
            }
            else
            {
                return bestMatch.child;
            }
        }

        private void RemoveImage(string imageId)
        {
            File.Delete(Path.Combine(path, imageId));
        }

        private string SaveImage(Bitmap image)
        {
            Guid guid = Guid.NewGuid();
            string imagePath = Path.Combine(path, guid.ToString());
            image.Save(imagePath, ImageFormat.Png );
            return guid.ToString();
        }

        public Bitmap LoadImage(string imageId)
        {
            return (Bitmap)Bitmap.FromFile(Path.Combine(path, imageId));
        }

        private double GetCosineSimilarity(double[] V1, double[] V2)
        {
            int N = 0;
            N = ((V2.Length < V1.Length) ? V2.Length : V1.Length);
            double dot = 0.0d;
            double mag1 = 0.0d;
            double mag2 = 0.0d;
            for (int n = 0; n < N; n++)
            {
                dot += V1[n] * V2[n];
                mag1 += Math.Pow(V1[n], 2);
                mag2 += Math.Pow(V2[n], 2);
            }

            return dot / (Math.Sqrt(mag1) * Math.Sqrt(mag2));
        }
    }
}
