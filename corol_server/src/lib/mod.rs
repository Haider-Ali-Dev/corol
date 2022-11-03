use models::Page;

pub mod models;
pub mod db;
pub fn sort(term: &str, pages: Vec<Page>) -> Vec<Page> {
    // Must be 10;
    let mut sorted_pages = vec![];
    for page in &pages {
        if sorted_pages.len() > 10 {
            break;
        }
        let page = page.clone();
        if page
            .clone()
            .description
            .unwrap_or("".to_owned())
            .contains(term)
        {
            sorted_pages.push(page)
        } else if page.clone().author.unwrap_or("".to_owned()).contains(term) {
            sorted_pages.push(page)
        } else if page.clone().title.unwrap_or("".to_owned()).contains(term) {
            sorted_pages.push(page)
        } else if page.clone().keywords.contains(&term.to_owned()) {
            sorted_pages.push(page)
        }
    }
    sorted_pages
}

#[cfg(test)]
mod test {
    macro_rules! some {
        ($a: expr) => {
            Some($a.to_owned())
        };
    }
    use crate::{models::Page, sort};
    #[test]
    fn test_sort() {
        let pages = vec![
            Page {
                id: uuid::Uuid::new_v4(),
                author: some!("Haider"),
                description: some!("Haider is a good human bean"),
                title: some!("Haider Ali"),
                keywords: vec![],
            },
            Page {
                id: uuid::Uuid::new_v4(),
                author: some!("Haider Ali Saeed"),
                description: some!("MIT"),
                title: some!("Saeed"),
                keywords: vec![],
            },
            Page {
                id: uuid::Uuid::new_v4(),
                author: some!("MIT"),
                description: some!("Best tech uni"),
                title: some!("MIT | Uni"),
                keywords: vec![],
            },
        ];
        let sorted = sort("MIT", pages);
        println!("{:?}", sorted);
        assert_eq!(sorted.len(), 2);
    }
}
