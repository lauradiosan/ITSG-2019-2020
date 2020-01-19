using Model;
using System;

namespace BusinessLayer.Interfaces
{
    public interface IAuthenticationController: IDisposable
    {
        Child LoggedInChild { get; }
        Child VisibleChild { get; }
        
        event EventHandler<Child> DetectedChild;
        event EventHandler<Child> ChildLoggedIn;
        event EventHandler<Child> ChildLoggedOut;

        void ForceLogout();
    }
}
