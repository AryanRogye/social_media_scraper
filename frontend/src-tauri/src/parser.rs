use std::error::Error;
extern crate serde;
extern crate serde_json;
use std::fs::File;
use std::io::Read;

#[allow(non_snake_case)]
#[derive(serde::Serialize, serde::Deserialize)]
#[derive(Default)]
pub struct User{
    #[serde(rename = "Instagram Account")]
    pub InstaAccount : String,
    pub Checked : bool
}

impl User {
    pub fn new(file : &str, limit: usize) -> Result<Vec<User>,Box<dyn Error>> {
        let new_user : Vec<User> = User::get_json_file(file, limit)?;
        Ok(new_user)
    }
    pub fn get_json_file(file : &str, limit : usize) -> Result<Vec<User>, Box<dyn Error>> {
        // So Basically We Need to parse the Json and only make sure we send back 10 unchecked
        let mut file = File::open(file)?;
        let mut buff = String::new();
        file.read_to_string(&mut buff)?;
        let new_user: Vec<User> = serde_json::from_str(&buff)?;
        // Limit to the limit
        // We can allocate on the stack cuz we know what the size is
        let unchecked_users: Vec<User> = new_user
            .into_iter()
            .filter(|user| !user.Checked)
            .take(limit)
            .collect();
        Ok(unchecked_users)
    }
}
