from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

def get_job_description(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    try:
        # Wait until the job description loads
        job_desc_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-automation-id="jobPostingDescription"]'))
        )
        job_desc = job_desc_element.text
    except Exception as e:
        job_desc = f"Could not extract description: {e}"

    driver.quit()
    return job_desc


def generate_cover_letter(job_description, model="llama3"):
    prompt = f"""
    Write a professional, one-page cover letter for the following job description:

    {job_description}

    Make it concise, enthusiastic, and tailored to the role. Assume the applicant has a background in Computer Information Systems and moderate Python proficiency.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt},
        stream=True  # streaming response
    )

    cover_letter = ""
    for line in response.iter_lines():
        if line:
            data = line.decode("utf-8")
            if data.strip().startswith("{"):
                obj = json.loads(data)
                cover_letter += obj.get("response", "")

    return cover_letter.strip()


if __name__ == "__main__":
    url = "https://wd1.myworkdaysite.com/recruiting/wf/WellsFargoJobs/job/CHARLOTTE-NC/XMLNAME-2026-Analytics-and-Data-Summer-Internship---Early-Careers_R-477788"
    description = get_job_description(url)
    print("Scraped Job Description:\n")
    print(description)
    
    cover_letter = generate_cover_letter(description, model="llama2")  # pass `description`
    print("\nGenerated Cover Letter:\n")
    print(cover_letter)
