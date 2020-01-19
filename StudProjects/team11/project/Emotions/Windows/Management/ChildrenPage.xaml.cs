using BusinessLayer.Interfaces;
using Emotions.CustomControlls;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows.Controls;
using Emotions.Utils;
using MaterialDesignThemes.Wpf;
using Services;

namespace Emotions.Windows.Management
{
    /// <summary>
    /// Interaction logic for ChildrenPage.xaml
    /// </summary>
    public partial class ChildrenPage : UserControl
    {
        public ChildrenPage(IChildrenController childrenController, ImageRecognitionService imageRecognitionService)
        {
            this.InitializeComponent();
            this.DataContext = new ChildrenPageViewModel(childrenController, imageRecognitionService);
        }
    }
}
