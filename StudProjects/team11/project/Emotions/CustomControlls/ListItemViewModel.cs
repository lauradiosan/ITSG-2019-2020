using Prism.Commands;
using System;
using System.Drawing;
using System.Windows;
using System.Windows.Input;
using System.Windows.Interop;
using System.Windows.Media.Imaging;

namespace Emotions.CustomControlls
{
    public abstract class ListItemViewModel : ListButton
    {
        public ListItemViewModel():base()
        {
            this.OnDelete = new DelegateCommand(this.Delete);
        }
        
        public int Id { get; set; }
        public string Name { get; set; }

        public virtual BitmapImage Icon
        {
            get; set;
        }

        public Visibility DeleteButtonVisibility { get; set; }

        public ICommand OnDelete { get; set; }

        public event EventHandler<ListItemViewModel> Deleted;

        private void Delete()
        {
            this.Deleted?.Invoke(this, this);
        }
    }
}
