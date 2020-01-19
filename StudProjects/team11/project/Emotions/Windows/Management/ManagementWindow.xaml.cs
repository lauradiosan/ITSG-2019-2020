using BusinessLayer;
using BusinessLayer.Interfaces;
using Emotions.Windows.Management.ViewModels;
using MaterialDesignThemes.Wpf;
using Prism.Commands;
using Services;
using System;
using System.Diagnostics;
using System.Windows;
using System.Windows.Controls.Primitives;
using System.Windows.Input;
using System.Windows.Media;

namespace Emotions
{
    /// <summary>
    /// Interaction logic for ManagementWindow.xaml
    /// </summary>
    public partial class ManagementWindow : Window
    {
        public ManagementWindow(ImageRecognitionService imageRecognitionService, IAppController appController, IChildrenController childrenController, IEmotionRecordingController emotionRecordingController)
        {
            this.InitializeComponent();

            this.DataContext = new ManagementWindowViewModel(appController, childrenController, imageRecognitionService, emotionRecordingController);
        }

        private void UIElement_OnPreviewMouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            //until we had a StaysOpen glag to Drawer, this will help with scroll bars
            var dependencyObject = Mouse.Captured as DependencyObject;
            while (dependencyObject != null)
            {
                if (dependencyObject is ScrollBar) return;
                dependencyObject = VisualTreeHelper.GetParent(dependencyObject);
            }

            this.MenuToggleButton.IsChecked = false;
        }

        public event EventHandler StartChildrenApp;

        

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            this.StartChildrenApp?.Invoke(this, EventArgs.Empty);
        }
    }
}
