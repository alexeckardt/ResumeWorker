import customtkinter as ctk
from main import runResumeScript

CLOSE_ON_UNFOCUS = True;

def run_main_function():
    
    input_text = text_entry.get("1.0", "end-1c")
    
    # inputData = getKeywords()
    
    inputData = {
        'positionName': text_jobTitle.get(),
        'companyName': text_compayName.get(),
        'locationState': text_locationState.get(),
        'jobDesc': input_text
    }
    
    runResumeScript(inputData)  # Call the main function from your module


def close_app(event):
    
    # Ensure that the app is unfocused
    if root.focus_get() is None:
        
        # Close the application
        if CLOSE_ON_UNFOCUS:
            root.destroy() 
            return;
        
        # Clear otherwise
        text_compayName.delete(0, "end")
        text_jobTitle.delete(0, "end")
        text_locationState.delete(0, "end")
        text_entry.delete("1.0", "end")



# Create the main window
root = ctk.CTk()
root.title("Simple Python Frontend")
root.geometry("400x400")
root.bind("<FocusOut>", close_app)

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark")  # Options: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Other options: "green", "dark-blue"

# Create an entry widget for text input
text_compayName = ctk.CTkEntry(root, placeholder_text="Company Name", width=300)
text_compayName.insert(0,'Google')
text_compayName.pack(pady=5)

text_jobTitle = ctk.CTkEntry(root, placeholder_text="Job Title", width=300)
text_jobTitle.insert(0,'Software Engineer')
text_jobTitle.pack(pady=5)

text_locationState = ctk.CTkEntry(root, placeholder_text="Location Distance (local,national,internation)", width=300)
text_locationState.insert(0,'local')
text_locationState.pack(pady=5)

label = ctk.CTkLabel(root, text="Job Description:")
label.pack(pady=(5,0))
text_entry = ctk.CTkTextbox(root, width=450, height=100)
text_entry.pack(pady=5)
job_description = '''Google's software engineers develop the next-generation technologies that change how billions of users connect, explore, and interact with information and one another. Our products need to handle information at massive scale, and extend well beyond web search. We're looking for engineers who bring fresh ideas from all areas, including information retrieval, distributed computing, large-scale system design, networking and data storage, security, artificial intelligence, natural language processing, UI design and mobile; the list goes on and is growing every day. As a software engineer, you will work on a specific project critical to Google’s needs with opportunities to switch teams and projects as you and our fast-paced business grow and evolve. We need our engineers to be versatile, display leadership qualities and be enthusiastic to take on new problems across the full-stack as we continue to push technology forward.
            Behind everything our users see online is the architecture built by the Technical Infrastructure team to keep it running. From developing and maintaining our data centers to building the next generation of Google platforms, we make Google's product portfolio possible. We're proud to be our engineers' engineers and love voiding warranties by taking things apart so we can rebuild them. We keep our networks up and running, ensuring our users have the best and fastest experience possible.
            With your technical expertise you will manage project priorities, deadlines, and deliverables. You will design, develop, test, deploy, maintain, and enhance software solutions.
            Google Cloud accelerates every organization's ability to digitally transform its business and industry. We deliver enterprise-grade solutions that leverage Google’s cutting-edge technology, and tools that help developers build more sustainably. Customers in more than 200 countries and territories turn to Google Cloud as their trusted partner to enable growth and solve their most critical business problems.
            The US base salary range for this full-time position is $161,000-$239,000 + bonus + equity + benefits. Our salary ranges are determined by role, level, and location. The range displayed on each job posting reflects the minimum and maximum target salaries for the position across all US locations. Within the range, individual pay is determined by work location and additional factors, including job-related skills, experience, and relevant education or training. Your recruiter can share more about the specific salary range for your preferred location during the hiring process.
                '''.replace('\n', ' ').replace('  ', ' ')
text_entry.insert("1.0", job_description)

# Create a button that will run the main function when clicked
run_button = ctk.CTkButton(root, text="Run", command=run_main_function)
run_button.pack(pady=10)

# Start the GUI loop
root.mainloop()