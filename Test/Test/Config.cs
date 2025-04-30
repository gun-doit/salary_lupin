using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace Test;

public class Config
{
    public string ProjectRoot { get; set; }
    public string OutputDir { get; set; }
    public string CssPath { get; set; }
    public bool IncludePrivateMembers { get; set; }
}

public static class ConfigLoader
{
    public static Config LoadConfig(string path)
    {
        // 프로젝트 루트 경로에서 config.json을 찾도록 설정
        var projectRoot = Directory.GetParent(Directory.GetCurrentDirectory()).Parent.Parent.FullName;
        var configPath = Path.Combine(projectRoot, path);

        // config.json 파일 읽기
        var json = File.ReadAllText(configPath);
        return JsonSerializer.Deserialize<Config>(json);
    }
}
