using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.StaticFiles;
using Microsoft.Extensions.DependencyInjection;
using System.IO;
using System.Net;
using System.Text;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", async (HttpContext context) =>
{
    var filePath = context.Request.Query["path"].ToString();
    if (string.IsNullOrEmpty(filePath))
    {
        context.Response.StatusCode = (int)HttpStatusCode.BadRequest;
        await context.Response.WriteAsync("File path is required.");
        return;
    }
    // Sanitize the filePath to prevent path traversal attacks
    // not working? also want to stop downloading application files
    filePath = filePath.Replace("../", "");
    filePath = filePath.Replace("/", "");
    filePath = WebUtility.UrlDecode(filePath);
    try
    {
        var provider = new Microsoft.AspNetCore.StaticFiles.FileExtensionContentTypeProvider();

        var contentType = "";
        if (!provider.TryGetContentType(filePath, out contentType))
        {
            contentType = "application/octet-stream"; // fallback content type
        }
        context.Response.ContentType = contentType;
        if (!contentType.StartsWith("image/"))
        {
            context.Response.Headers.Add("Content-Disposition", $"attachment; filename=\"{filePath}\"");
        }
        await context.Response.SendFileAsync(filePath);
    }
    catch (FileNotFoundException)
    {
        context.Response.StatusCode = (int)HttpStatusCode.NotFound;
        await context.Response.WriteAsync("File not found");
    }
    catch (Exception)
    {
        context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;
        await context.Response.WriteAsync("An error occurred");
    }
});


app.MapPost("/upload", async (HttpContext context) =>
{
    if (!context.Request.HasFormContentType || !context.Request.Form.Files.Any())
    {
        context.Response.StatusCode = (int)HttpStatusCode.BadRequest;
        await context.Response.WriteAsync("No files uploaded.");
        return;
    }

    var file = context.Request.Form.Files[0];

    const long maxUploadFileSize = 10 * 1024 * 1024; // 10 MB

    if (file.Length > maxUploadFileSize)
    {
        context.Response.StatusCode = (int)HttpStatusCode.RequestEntityTooLarge;
        await context.Response.WriteAsync("Uploaded file size exceeds the allowed limit.");
        return;
    }
    var filename = context.Request.Form["filename"].ToString();

    // Sanitize the file name to prevent path traversal attacks
    var uploadPath = filename.Replace("../", "");

    try
    {
        using var stream = new FileStream(uploadPath, FileMode.Create);
        await file.CopyToAsync(stream);

        context.Response.StatusCode = (int)HttpStatusCode.OK;
        await context.Response.WriteAsync(uploadPath);
    }
    catch (Exception)
    {
        context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;
        await context.Response.WriteAsync("An error occurred");
    }
});

app.Run();

