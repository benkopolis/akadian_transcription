using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Microsoft.Office.Interop.Word;
using System.Text.RegularExpressions;

namespace ExtractCommentedText
{
    public class Program
    {
        internal static void GetCommentsFromDocument(string fileName)
        {
            Application app = new Application();
            Document doc = app.Documents.Open(fileName);
            if (doc.Comments.Count == 0)
                return;
            Dictionary<string, List<string>> labels = new Dictionary<string, List<string>>();
            foreach(Comment comment in doc.Comments)
            {
                string lbl = Regex.Replace(comment.Range.Text, @"\s+", "");
                if (!labels.ContainsKey(lbl))
                    labels.Add(lbl, new List<string>());
                labels[lbl].Add(comment.Scope.Text.Trim());
            }
            var systemPath = System.Environment.
                             GetFolderPath(
                                 Environment.SpecialFolder.CommonApplicationData
                             );
            Console.WriteLine($"Files will be created at '{systemPath}', is that ok? (Y or y for yes, otherwise program will stop): ");
            var key = Console.ReadKey();
            if (key.KeyChar != 'Y' && key.KeyChar != 'y')
                return;
            foreach (string label in labels.Keys)
            {
                if (!File.Exists(label))
                {
                    // Create a file to write to.
                    using (StreamWriter sw = File.CreateText(Path.Combine(systemPath, $"{label}.txt")))
                    {
                        sw.WriteLine("=@#$%^&*&^%$#@=");
                        foreach (string t in labels[label])
                        {
                            sw.WriteLine(t);
                            sw.WriteLine("=@#$%^&*&^%$#@=");
                        }
                    }
                }

                string result = "";
                result = string.Format("{0}:", label);
                

                Console.WriteLine(result);
            }
        }

        static void Main(string[] args)
        {
            if (args.Length < 1)
            {
                Console.WriteLine("Please provide filename as an input parameter");
                return;
            }

            GetCommentsFromDocument(args[0]);
            Console.ReadKey();
        }
    }
}
