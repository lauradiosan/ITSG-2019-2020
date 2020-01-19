using Model;
using System.Collections.Generic;
using System.Drawing;

namespace BusinessLayer.Interfaces
{
    public interface IChildrenController
    {
        List<Child> GetAllChildren();
        void AddChild(Child child, Bitmap image);
        void RemoveChild(int id);
        Child GetChildByYhat(double[] yhat);
        Bitmap LoadImage(string imageId);
    }
}
