using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Dwm;

namespace Dwm
{
    public class ThumbnailEx : Thumbnail
    {
        /// <summary>
        /// Creates a new thumbnail given a destination form handle and a source form handle
        /// </summary>
        /// <param name="hwndDestination">Handle of the form where the thumbnail will appear</param>
        /// <param name="hwndSource">Handle of the form for which the thumbnail is created</param>
        public ThumbnailEx(IntPtr hwndDestination, IntPtr hwndSource) : base(hwndDestination, hwndSource)
        {
        }

        /// <summary>
        /// Creates a new thumbnail given a destination form and a source form handle
        /// </summary>
        /// <param name="destination">Form where the thumbnail will appear</param>
        /// <param name="hwndSource">Handle of the form for which the thumbnail is created</param>
        public ThumbnailEx(Form destination, IntPtr hwndSource) : base(destination, hwndSource)
        {
        }

        public ThumbnailEx(IntPtr hwndDestination, int hwndSource) : base(hwndDestination, new IntPtr(hwndSource))
        {
        }

        public ThumbnailEx(int dest, int source): base(new IntPtr(dest), new IntPtr(source)) { }

        /// <summary>
        /// Creates a new thumbnail given a destination form and a source form
        /// </summary>
        /// <param name="destination">Form where the thumbnail will appear</param>
        /// <param name="source">Form for which the thumbnail is created</param>
        public ThumbnailEx(Form destination, Form source) : base(destination, source)
        {
        }
    }
}
