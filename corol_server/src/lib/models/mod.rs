use serde::{Serialize, Deserialize};
use uuid::Uuid;


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Page {
    pub id: Uuid,
    pub author: Option<String>,
    pub description: Option<String>,
    pub title: Option<String>,
    pub keywords: Vec<String>
}

 
