using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace Test.Document;

public static class MarkdownWriter
{

    public static string[] PrimitiveType =
    {
        "Bool", "Byte", "SByte", "Short", "UShort",
        "Object", "Int", "UInt", "Long", "ULong",
        "Float", "Double", "Decimal", "Char", "String",
    };
    public static void code(this List<String> Line, string code) => Line.Add($"```csharp\n{code}\n```");
    public static void text(this List<String> Line, string text) => Line.Add(text);
    public static void h1(this List<String> Line, string text) => Line.Add($"# {text}");
    public static void h2(this List<String> Line, string text) => Line.Add($"## {text}");
    public static void h3(this List<String> Line, string text) => Line.Add($"### {text}");

    public static void quote(this List<String> Line, string text) => Line.Add($"> {text}");
    public static void newLine(this List<String> Line) => Line.Add("");
    public static void bold(this List<String> Line, string text) => Line.Add($"** {text} **");
    public static void indent(this List<String> Line, string text) => Line.Add($"- {text}");

    public static string islink(this List<String> Line, string text)
    {
        // class
        if (PrimitiveType.Contains(text)) return text;
        else
        {
            if (Analyzer.ClassDictionary.ContainsKey(text)) return text;
            else return "Unkown Type";
        }
    }
}
