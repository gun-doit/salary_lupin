using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection.Metadata;
using Test.Document;

public class Analyzer
{
    public static Dictionary<string, string> ClassDictionary = new();
    /// <summary>
    /// .cs 파일 분석
    /// </summary>
    /// <param name="file"></param>
    /// <param name="projectRoot"></param>
    /// <param name="outputDir"></param>
    public void AnalyzeFile(string file, string projectRoot, string outputDir)
    {
        var code = File.ReadAllText(file);
        var tree = CSharpSyntaxTree.ParseText(code);
        var root = tree.GetRoot();

        List<string> Markdown = new();

        var nameSpaceDeclaration = root.DescendantNodes().OfType<NamespaceDeclarationSyntax>().FirstOrDefault();
        var nameSpace = nameSpaceDeclaration?.Name.ToString();
        var classDeclaration = root.DescendantNodes().OfType<ClassDeclarationSyntax>().FirstOrDefault();
        if (classDeclaration == null || nameSpace == null)
            return;

        var className = classDeclaration.Identifier.Text;
        var classSummary = GetSummaryComment(classDeclaration);
        var classSignature = GetClassDeclaration(classDeclaration);
   
        Markdown.h1(className);
        Markdown.text($"Path: {file}");
        Markdown.text($"네임스페이스 : {nameSpace}");
        Markdown.newLine();

        if (!string.IsNullOrEmpty(classSummary))
        {
            Markdown.quote(classSummary);
            Markdown.newLine();
        }

        Markdown.h2("Class Declaration");
        Markdown.code(classSignature);

        // Constructor
        var constructors = classDeclaration.Members.OfType<ConstructorDeclarationSyntax>().ToList();
        if (constructors.Any())
        {
            Markdown.newLine();
            Markdown.h2("Constructor");
            foreach (var ctor in constructors)
            {
                Markdown.code(ctor.ToFullString());
            }
        }

        // Methods
        var methods = classDeclaration.Members.OfType<MethodDeclarationSyntax>().ToList();
        if (methods.Any())
        {
            Markdown.newLine();
            Markdown.h2("Methods");

            foreach (var method in methods)
            {
                var methodName = method.Identifier.Text;
                var methodSummary = GetSummaryComment(method);
                var methodDeclaration = GetMethodDeclaration(method);

                Markdown.h3(methodName);

                if (!string.IsNullOrEmpty(methodSummary))
                {
                    Markdown.quote(methodSummary);
                }

                Markdown.code(methodDeclaration);

                var paramComments = GetParamComments(method);

                if (method.ParameterList.Parameters.Count > 0)
                {
                    Markdown.bold("Parameters");
                    foreach (var param in method.ParameterList.Parameters)
                    {
                        var paramName = param.Identifier.Text;
                        var paramType = param.Type?.ToString();

                        if (PrimitiveType.Contains(paramType))
                        Markdown.indent($"{paramName} ({paramType})");

                        if (paramComments.TryGetValue(paramName, out var comment) && !string.IsNullOrWhiteSpace(comment))
                        {
                            Markdown.quote(comment);
                        }
                    }
                }

                Markdown.newLine();
            }
        }

        // 상대 경로 기반 출력 경로 설정
        var relativePath = Path.GetRelativePath(projectRoot, file);
        var outputFilePath = Path.Combine(outputDir, Path.ChangeExtension(relativePath, ".md"));

        var outputFileDir = Path.GetDirectoryName(outputFilePath);
        if (!Directory.Exists(outputFileDir))
            Directory.CreateDirectory(outputFileDir);

        File.WriteAllText(outputFilePath, string.Join(Environment.NewLine, Markdown));
    }
    public void AnalyzeClass(string file, string projectRoot, string outputDir)
    {
        var code = File.ReadAllText(file);
        var tree = CSharpSyntaxTree.ParseText(code);
        var root = tree.GetRoot();

        var classDeclaration = root.DescendantNodes().OfType<ClassDeclarationSyntax>().FirstOrDefault();
        if (classDeclaration == null)
            return;

        var className = classDeclaration.Identifier.Text;

        // 상대 경로 기반 출력 경로 설정
        var relativePath = Path.GetRelativePath(projectRoot, file);
        var outputFilePath = Path.Combine(outputDir, Path.ChangeExtension(relativePath, ".md"));

        ClassDictionary.Add(className, outputFilePath);
        Console.WriteLine(outputFilePath);
    }
    public void AnalyzeProject(string projectPath, string outputDir)
    {
        var csFiles = Directory.GetFiles(projectPath, "*.cs", SearchOption.AllDirectories);

        foreach (var file in csFiles)
        {
            AnalyzeClass(file, projectPath, outputDir); // projectPath 추가로 넘김
        }

        foreach (var file in csFiles)
        {
            AnalyzeFile(file, projectPath, outputDir); // projectPath 추가로 넘김
        }
    }

    // 클래스 선언문 생성/
    private string GetClassDeclaration(ClassDeclarationSyntax classSyntax)
    {
        return classSyntax.ToString().Split(new[] { '{' }, 2)[0].Trim(); // 바디 제외 선언문만
    }

    // 메서드 선언문 생성
    private string GetMethodDeclaration(MethodDeclarationSyntax methodSyntax)
    {
        return methodSyntax.ToString().Split(new[] { '{' }, 2)[0].Trim(); // 바디 제외 선언문만
    }

    // <summary> 태그 추출
    private string GetSummaryComment(MemberDeclarationSyntax member)
    {
        var trivia = member.GetLeadingTrivia();

        var xmlDocComment = trivia
            .Select(t => t.GetStructure())
            .OfType<DocumentationCommentTriviaSyntax>()
            .FirstOrDefault();

        if (xmlDocComment != null)
        {
            var summaryElement = xmlDocComment.Content
                .OfType<XmlElementSyntax>()
                .FirstOrDefault(element => element.StartTag.Name.LocalName.Text == "summary");

            if (summaryElement != null)
            {
                return summaryElement.Content.ToString().Trim().Replace("///", "");
            }
        }

        return string.Empty;
    }
    private Dictionary<string, string> GetParamComments(SyntaxNode member)
    {
        var result = new Dictionary<string, string>();

        var xmlDocComment = member.DescendantTrivia()
            .FirstOrDefault(t => t.IsKind(SyntaxKind.SingleLineDocumentationCommentTrivia) ||
                                 t.IsKind(SyntaxKind.MultiLineDocumentationCommentTrivia));

        if (xmlDocComment != default)
        {
            var structure = xmlDocComment.GetStructure() as DocumentationCommentTriviaSyntax;
            if (structure != null)
            {
                var paramElements = structure.Content
                    .OfType<XmlElementSyntax>()
                    .Where(el => el.StartTag.Name.LocalName.Text == "param");

                foreach (var param in paramElements)
                {
                    var nameAttr = param.StartTag.Attributes
                        .OfType<XmlNameAttributeSyntax>()
                        .FirstOrDefault(attr => attr.Name.LocalName.Text == "name");

                    if (nameAttr != null)
                    {
                        var paramName = nameAttr.Identifier.Identifier.ValueText;
                        var paramText = param.Content.ToString().Trim();
                        result[paramName] = paramText;
                    }
                }
            }
        }

        return result;
    }
}
