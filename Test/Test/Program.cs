
using System;
using Test;

class Program
{
    static void Main(string[] args)
    {
        {
            var config = ConfigLoader.LoadConfig("config.json");

            var analyzer = new Analyzer();
            analyzer.AnalyzeProject(config.ProjectRoot, config.OutputDir);

            Console.WriteLine("Documentation generated successfully for all files!");
        }
    }

}