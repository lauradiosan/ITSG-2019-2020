using BusinessLayer.Interfaces;
using MaterialDesignThemes.Wpf;
using Prism.Commands;
using Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;

namespace Emotions.Windows.Management.ViewModels
{
    public class ManagementWindowViewModel
    {
        public ManagementWindowViewModel(IAppController appController, IChildrenController childrenController, ImageRecognitionService imageRecognitionService, IEmotionRecordingController emotionRecordingController)
        {
            this.Pages = new[] {
                new PageItem("Apps", new ApplicationsPage(appController)),
                new PageItem("Children", new ChildrenPage(childrenController, imageRecognitionService)),
                new PageItem("Sessions", new SessionDataPage(emotionRecordingController, childrenController))
            };
        }
        
        public PageItem[] Pages { get; }
    }
}
