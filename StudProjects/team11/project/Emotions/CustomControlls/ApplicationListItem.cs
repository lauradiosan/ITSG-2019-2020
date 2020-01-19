using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Interop;
using System.Windows.Media.Imaging;
using Emotions.Utils;
namespace Emotions.CustomControlls
{
    public class ApplicationListItem : ListItemViewModel
    {
        private BitmapImage icon;

        public ApplicationListItem() : base()
        {
        }

        public string Path { get; set; }

        public override BitmapImage Icon
        {
            get
            {
                if (this.icon == null)
                {
                    using (Icon ico = System.Drawing.Icon.ExtractAssociatedIcon(this.Path))
                    {
                        this.icon = ico.ToBitmapImage();
                    }
                }
                return this.icon;
            }
        }
    }
}
