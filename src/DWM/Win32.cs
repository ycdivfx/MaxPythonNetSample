using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace Dwm
{
    [StructLayout(LayoutKind.Sequential)]
    public struct Rect
    {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    public class Win32
    {
        [DllImport("user32.dll")]
        private static extern bool GetWindowRect(IntPtr hWnd, out Rect lpRect);

        [DllImport("user32.dll")]
        private static extern bool GetClientRect(IntPtr hWnd, out Rect lpRect);

        public static Rectangle GetWindowsRectangle(int hwnd)
        {
            Rect lpRect;
            GetWindowRect(new IntPtr(hwnd), out lpRect);
            return new Rectangle(lpRect.Left, lpRect.Top, lpRect.Right, lpRect.Bottom);
        }

        public static Rectangle GetClientRectangle(int hwnd)
        {
            Rect lpRect;
            GetClientRect(new IntPtr(hwnd), out lpRect);
            return new Rectangle(lpRect.Left, lpRect.Top, lpRect.Right, lpRect.Bottom);
        }
    }
}
