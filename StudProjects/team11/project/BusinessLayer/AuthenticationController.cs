using BusinessLayer.Interfaces;
using Model;
using Services;
using System;
using System.Threading;

namespace BusinessLayer
{
   public class AuthenticationController : IAuthenticationController, IDisposable
    {
        IChildrenController childrenController;
        ImageRecognitionService imageRecognitionService;

        TimeSpan msToLogin;
        TimeSpan msToLogout;

        private Face currentFace;
        private DateTime? timeAppeared;
        private Thread identityThread;

        public AuthenticationController(IChildrenController childrenController, ImageRecognitionService imageRecognitionService,int msToLogin, int msToLogout)
        {
            this.imageRecognitionService = imageRecognitionService;
            this.childrenController = childrenController;
            this.LoggedInChild = null;
            this.VisibleChild = null;

            this.msToLogin = TimeSpan.FromMilliseconds(msToLogin);
            this.msToLogout = TimeSpan.FromMilliseconds(msToLogout);


            this.imageRecognitionService.ImageReceived += this.ImageRecognitionService_ImageReceived;

            this.identityThread = new Thread(this.ProcessFrames);
            this.identityThread.Name = "IdentitySericeThread";
            this.identityThread.Priority = ThreadPriority.AboveNormal;
            this.identityThread.Start();
        }

        public void ForceLogout()
        {
            this.LoggedInChild = null;
            this.timeAppeared = null;
            this.ChildLoggedOut?.Invoke(null, null);
        }
        
        public Child LoggedInChild { get; private set; }
        public Child VisibleChild { get; private set; }

        public event EventHandler<Child> DetectedChild;
        public event EventHandler<Child> ChildLoggedIn;
        public event EventHandler<Child> ChildLoggedOut;
        
        private void ImageRecognitionService_ImageReceived(object sender, Face e)
        {
            this.currentFace = e;
        }

        private void ProcessFrames()
        {
            while (true)
            {
                Child detectedChild = null;
                try
                {
                    if (this.currentFace != null && this.currentFace.Yhat != null)
                    {
                        detectedChild = this.childrenController.GetChildByYhat(this.currentFace.Yhat);
                    }
                    else
                    {
                        Thread.Sleep(100);
                    }
                }
                finally
                {
                    this.DetectedChild?.Invoke(this, detectedChild);
                    this.VisibleChild = detectedChild;
                    this.CheckTimeOnScreen(detectedChild);
                }
            }
        }

        private void CheckTimeOnScreen(Child detectedChild)
        {
            if (detectedChild != this.LoggedInChild)
            {
                if (!this.timeAppeared.HasValue)
                {
                   this.timeAppeared = DateTime.Now;
                }

                TimeSpan timeOnScreen = DateTime.Now.Subtract(this.timeAppeared.Value);
                if (this.LoggedInChild != null && timeOnScreen > this.msToLogout)
                {
                    this.ChildLoggedOut?.Invoke(this, this.LoggedInChild);
                    this.LoggedInChild = null;
                    this.timeAppeared = DateTime.Now;
                    return;
                }

                if (detectedChild != null && this.LoggedInChild == null && timeOnScreen > this.msToLogin)
                {
                    this.LoggedInChild = detectedChild;
                    this.ChildLoggedIn?.Invoke(this, this.LoggedInChild);
                    this.timeAppeared = DateTime.Now;
                    return;
                }
            }
            else
            {
                this.timeAppeared = null;
            }
        }

        #region IDisposable Support
        private bool disposedValue = false; // To detect redundant calls

        protected virtual void Dispose(bool disposing)
        {
            if (!this.disposedValue)
            {
                if (disposing)
                {
                    this.identityThread.Abort();
                }

                this.disposedValue = true;
            }
        }

        public void Dispose()
        {
            this.Dispose(true);
        }
        #endregion
    }

}
