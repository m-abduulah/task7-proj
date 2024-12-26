Project Overview
This project aimed to enhance an existing MLOps pipeline by integrating advanced tools to manage machine learning processes. The goal was to develop a temperature forecasting model using meteorological data. The key tools employed were:

DVC (Data Version Control): Used for versioning and tracking data changes, promoting reproducibility and collaboration by enabling easy retrieval of past datasets.
MLFlow: Utilized for model management, including experiment tracking, model versioning, and transitioning models from development to production.
Airflow: Implemented to automate and schedule workflows, such as data collection, preparation, and model training, ensuring continuous data flow into the system.
The project focused on integrating these tools within a full-stack application and setting up CI/CD pipelines using Docker and Kubernetes.

Objectives
The main objectives of the project were to:

Implement DVC: Use nested versioning to efficiently manage large datasets and model files, allowing for version control similar to Git but tailored for data science.
Utilize MLFlow for Model Management: Monitor experiments, log parameters and metrics, and manage model lifecycle. This includes creating a model registry for versioning and quick deployment or rollback.
Automate with Airflow: Automate data collection, preprocessing, and model training, while scheduling complex workflows for efficient MLOps management.
By achieving these goals, the project aimed to highlight the importance of contemporary MLOps tools and their strategic applications in machine learning workflows.

Project Workflow and Tools

DVC (Data Version Control): DVC facilitated the management and versioning of large datasets and models, ensuring data consistency across multiple developers. It enabled seamless synchronization of changes, preventing conflicts in a collaborative environment.
MLFlow: MLFlow was used to track machine learning experiments and their parameters. The Model Registry feature allowed us to manage models through different stages (development, staging, production) and easily revert to previous versions, ensuring optimal model quality and organization.
Airflow: Airflow automated and scheduled tasks such as data collection and preprocessing on an hourly basis, reducing manual effort and ensuring timely updates to the data feeding into the models.
Git: Git managed source code versioning, supporting features like branches, merges, and pull requests, which were crucial for collaboration within a team of multiple developers.
Docker and Kubernetes: Docker was used to containerize the application, ensuring consistent performance across different systems. Kubernetes orchestrated the containers, handling scaling, management, and lifecycle during development and deployment.
Windows: Development on Windows posed compatibility issues, which were mitigated by containerizing the application with Docker, providing a consistent development environment across various operating systems.
Data Collection and Preprocessing

Collecting Data: Airflow was used to automate the data collection process, retrieving real-time weather data from the OpenWeatherMap API for Islamabad. The data included key variables such as temperature, humidity, wind speed, and other meteorological factors, all of which were essential for the predictive model. Automation ensured that data was consistently gathered and updated without manual intervention, keeping the model aligned with current conditions.
import requests
import pandas as pd

# Define API-related constants
API_KEY = "your-api-key"  
CITY_NAME = "London"
LATITUDE = 35.7721  
LONGITUDE = -78.63861  
API_ENDPOINT = "https://api.weatherbit.io/v2.0/history/daily"

def fetch_data():
    """
    Fetch historical weather data for the past year from the Weatherbit API.
    """
    # Determine the date range (1 year back from today)
    today = datetime.now()
    one_year_ago = today - timedelta(days=50)

    # Placeholder for daily weather data
    collected_data = []

    # Loop through each day in the date range
    current_day = one_year_ago
    while current_day < today:
        # Format dates as strings in YYYY-MM-DD
        start_date = current_day.strftime("%Y-%m-%d")
        next_date = (current_day + timedelta(days=1)).strftime("%Y-%m-%d")

        # Configure query parameters
        query_parameters = {
            "lat": LATITUDE,
            "lon": LONGITUDE,
            "start_date": start_date,
            "end_date": next_date,
            "key": API_KEY,
        }

        # Request weather data from the API
        response = requests.get(API_ENDPOINT, params=query_parameters)

        if response.status_code == 200:
            weather_response = response.json()

            # Ensure the response contains data
            if "data" in weather_response and weather_response["data"]:
                weather_entry = weather_response["data"][0]
                daily_weather = {
                    "Date": start_date,
                    "Temperature (\u00b0C)": weather_entry.get("temp"),
                    "Max Temperature (\u00b0C)": weather_entry.get("max_temp"),
                    "Min Temperature (\u00b0C)": weather_entry.get("min_temp"),
                    "Humidity (%)": weather_entry.get("rh"),
                    "Wind Speed (m/s)": weather_entry.get("wind_spd"),
                    "Precipitation (mm)": weather_entry.get("precip", 0),
                    "Cloud Cover (%)": weather_entry.get("clouds", 0),
                }
                collected_data.append(daily_weather)
            else:
                print(f"No weather data available for {start_date}")
        else:
            print(f"Error fetching data for {start_date}: {response.status_code} - {response.text}")

        # Proceed to the next day
        current_day += timedelta(days=1)

    # Export the collected data to a CSV file
Preprocessing Data

The retrieved data was standardized using a StandardScaler in our preprocessing script. This transformation ensured that the input features were on a consistent scale, which is crucial for accurate predictions. Standardizing the data helped maintain uniformity across different features, preparing it for optimal performance in the machine learning model.

Workflow Automation with Airflow

Airflow Pipeline
Our entire workflow, from data collection to preparation, was automated using Airflow. The pipeline was scheduled to run on an hourly basis, ensuring that the dataset was continuously updated and ready for training. This automation minimized the gap between data collection and model training, helping maintain the model’s accuracy and relevance by reducing latency.

Model Training and Monitoring

Training with MLFlow
In the training.py script, we developed a linear regression model to predict temperatures based on wind speed and humidity. MLFlow’s autolog feature played a key role by automatically logging all aspects of the training session, including model parameters and performance metrics. This setup allowed us to track the model's performance over time, ensuring continuous monitoring and improvements.

DVC in Model Versioning

DVC enabled us to manage the version history of both datasets and models effectively. Google Drive served as our remote storage, and DVC ensured that we could monitor changes and maintain reproducibility across experiments. By integrating DVC, we were able to:

Monitor Changes in the Dataset: Track modifications in data sources and easily revert to previous versions if newer data negatively impacted model performance.
Model Versioning: Link specific datasets with model versions to identify which combinations led to the best-performing models.
Experiment Logs: Maintain detailed records of experimental configurations and outcomes, facilitating better parameter tuning based on historical results.
dvc add data/dataset.csv
dvc push
Docker and Kubernetes

Starting Minikube
- name: Start Minikube run: | minikube start --driver=docker
In this step, we start Minikube to create a local Kubernetes cluster using Docker as the container runtime. Minikube simulates a Kubernetes environment on your local machine, making it ideal for development and testing. The --driver=docker option ensures that Docker is used as the driver, eliminating the need for a separate virtual machine and integrating the setup seamlessly with the existing Docker configuration.
Pulling the Docker Image
- name: Pull Docker image
  run: |
    docker pull ${{ secrets.DOCKER_USERNAME }}/class-act-7:latest
Here, we pull the latest Docker image of our application from a Docker registry. This ensures that the Kubernetes cluster is using the most up-to-date version of the application. The secret key ${{ secrets.DOCKER_USERNAME }} is used to securely access the Docker account, highlighting how sensitive data can be managed safely within Kubernetes deployments.
Deploying the Application
- name: Deploy application to Kubernetes
  run: |
    kubectl create deployment test-app --image=${{ secrets.DOCKER_USERNAME }}/class-act-7:latest
    kubectl expose deployment test-app --type=NodePort --port=9875
This step deploys the application to the Kubernetes cluster. The kubectl create deployment command sets up the necessary pods with the Docker image, ensuring a scalable deployment. Afterward, the kubectl expose command makes the application accessible outside the Kubernetes cluster. Using the NodePort type exposes the application on a port across all nodes, enabling external access to the service, which is crucial for real-world applications requiring external user access.
Frontend Development

The frontend of the application provides a user-friendly interface for interacting with the prediction system, designed with the following components:

Technologies Used: The frontend is built using HTML and CSS, with an optional frontend framework for JavaScript to enhance interactivity.
Key Features:
User Forms: Forms for user login and signup, allowing users to create accounts and access the system.
Weather Data Input: Forms for inputting weather data, specifically humidity and wind speed, which are used for generating temperature predictions.
Prediction Display: After the user submits the form, the frontend displays the predicted temperature based on the inputs for humidity and wind speed.
Frontend-Backend Interaction: The frontend captures user inputs and sends them to the backend for processing. The backend then generates the temperature prediction based on the input data and returns the result to the frontend for display.
You can view a demo of the frontend application through the following link:

bandicam 2024-12-16 14-20-11-042.mp4
Demo Video drive.google.com

Key Learnings

Insights on MLOps Tools

The integration and application of MLOps tools like DVC, MLFlow, and Airflow provided valuable insights into how these technologies enhance machine learning projects. Each tool offered unique strengths, and together they formed an effective system for managing the entire ML pipeline:

DVC (Data Version Control): DVC enabled us to systematically track data and model changes. It facilitated collaboration by allowing team members to share updates without the risk of overwriting each other’s work, making it easier to replicate and record experiments. This tool played a crucial role in maintaining the integrity of data and model versions, ensuring reproducibility.
MLFlow: MLFlow helped us track and manage the lifecycle of machine learning models. It allowed us to monitor experiments, compare model performance, and make informed decisions about promoting models to production. The Model Registry in MLFlow provided a reliable repository for storing models, making it seamless to transition models from development to production environments.
Airflow: Airflow streamlined the execution of data pipelines by automating processes like data fetching, preprocessing, and model training. With its scheduling and task orchestration capabilities, Airflow minimized manual effort, reduced the risk of errors, and ensured that data and models were always up to date.
Together, these tools provided a robust framework for managing the full ML lifecycle, from data collection and model training to deployment and monitoring.

Reflecting on MLOps Practices

This project has highlighted the benefits of incorporating MLOps practices, revealing several key takeaways:

Efficiency and Scalability: Automation of data gathering, preparation, and model training pipelines allowed us to scale the project without increasing manual effort. This significantly improved efficiency and minimized errors.
Reproducibility and Accountability: By integrating DVC and MLFlow, all experiments were properly versioned and tracked, ensuring that no work was lost and that models could be traced back to their authors. This systematic approach improved accountability and reproducibility.
Real-Time Data Handling: Airflow enabled real-time data processing, ensuring that our forecasting models remained relevant and accurate. This capability was essential for handling dynamic, real-time data.
Collaboration and Communication: MLOps tools fostered better collaboration by making it easy for team members to share progress, results, and outcomes. This improved communication within the team and allowed for more effective collaboration.
In conclusion, the integration of MLOps tools not only addressed the technical needs of the project but also fostered a culture of continuous improvement and learning. MLOps is more than just a set of technologies — it is a framework that applies best practices to create high-quality, reproducible, and scalable machine learning models.
