import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from hospital_ops.tools.custom import list_hospitals_tool, get_hospital_path_tool, recall_context_tool
from hospital_ops.tools.imported import read_file_tool

@CrewBase
class HospitalOpsCrew():
	"""HospitalOps crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	os.environ["OPENAI_MODEL_NAME"]="gpt-4o"
     
	@agent
	def senior_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['senior_analyst'],
			tools=[recall_context_tool, list_hospitals_tool, get_hospital_path_tool, read_file_tool],
			verbose=True
		)
  
	# @agent
	# def data_assistant(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['data_assistant'],
	# 		tools=[list_hospitals_tool, get_hospital_path_tool, read_file_tool],
	# 		verbose=True
	# 	)

	@task
	def analysing_hospital_operations_task(self) -> Task:
		return Task(
			config=self.tasks_config['analysing_hospital_operations_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the HospitalOps crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)