mod parser;
use parser::User;
use std::{
    error::Error, 
    env, 
};
use serde_json::to_string;
use tokio::process::Command;


async fn call_sel_py(users_json_str: String, file: &str) -> Result<(), Box<dyn Error>> {
    let curr_dir = std::env::current_dir().expect("Failed to get the current dir");
    let script_path = curr_dir.join("src-tauri/sel_py");
    println!("Got File -- {}", file);

    println!("Executing {:?}", script_path);
    let mut child = Command::new("sh")
        .arg(script_path)
        .arg(users_json_str)
        .arg(file)
        .spawn()?;

    // Wait for the child process to complete in a separate async task
    tokio::spawn(async move {
        match child.wait().await {
            Ok(status) if status.success() => {
                println!("Everything ran successfully");
            }
            Ok(status) => {
                eprintln!("Subprocess failed with status: {}", status);
            }
            Err(e) => {
                eprintln!("Failed to wait on subprocess: {}", e);
            }
        }
    });

    // Immediately return to allow the frontend to continue
    Ok(())
}

#[tauri::command]
async fn open_sel(json_data: String, file: &str) -> Result<String, String> {
    println!("Received JSON Data: {}", json_data);
    match call_sel_py(json_data, file).await {
        Ok(_) => Ok("Opened".to_string()),
        Err(e) => Err(e.to_string())
    }
}

async fn handle_txt(file: &str, limit: usize) -> Result<String, Box<dyn std::error::Error>> {
    let users = User::new(file, limit)?;
    //call_sel_py(users).await.expect("Couldnt Execute User");
    Ok(to_string(&users)?)
}

#[tauri::command]
async fn parse_file(file: &str, limit: usize) -> Result<String, String> {
    // Check the extension first
    println!("Got Limit -- {}", limit);
    if file.ends_with(".json") {
        println!("Parsing Started");
        match handle_txt(file, limit).await {
            Ok(user) => Ok(String::from(user)),
            Err(e) => {
                println!("There was an Error: {}", e);
                Err(format!("Error: {}", e))
            }
        }
    } else {
        Err("File type cannot be parsed yet. Sorry :(".to_string())
    }
}

#[tauri::command]
fn open_finder() -> String {
    use rfd::FileDialog;
    if let Some(files) = FileDialog::new()
        .add_filter("text", &["txt", "json", "log"])
        .set_directory(".")
        .pick_file()
    {
        return format!("{}", files.to_string_lossy())
    } else {
        return "None".to_string()
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![open_finder, parse_file, open_sel])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
