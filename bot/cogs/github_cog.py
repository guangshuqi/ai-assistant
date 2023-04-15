#bot/cogs/github_cog.py
from discord.ext import commands
from github import Github
from config import GITHUB_TOKEN
from utils.message_splitter import split

REPO_OWNER = "guangshuqi"
REPO_NAME = "ai-assistant"
class GithubCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github = Github(GITHUB_TOKEN)

    @commands.command()
    async def readfile(self, ctx, file_path):
        """
        Read a file from a GitHub repository.
        Input: file_path
        """
        print('readfile')
        # Read the file
        repo = self.github.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
        print(file_path)
        file_content = repo.get_contents(file_path)
        print(file_content)
        decoded_content = file_content.decoded_content.decode("utf-8")
        print(decoded_content)
        # Send the response
        content = f"File content of {file_path}:\n```{decoded_content}```"
        for chunk in split(content):
            await ctx.send(chunk)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command()
    async def listfile(self, ctx):
        '''
        list all files in a GitHub repository.
        input: None
        '''
        repo = self.github.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

        files = recursive_list_files(repo, '')
        files_string = '\n'.join(files)
        # Send the response
        await ctx.send(f"Files {files_string}")
    # Add more commands for other GitHub functionalities here, like editfile and createpr.

    @commands.command()
    async def createbranch(self, ctx, branch_name):
        '''
        create a new branch in a GitHub repository.
        input: branch_name
        '''
        repo = self.github.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=repo.get_branch("main").commit.sha)
        await ctx.send(f"branch {branch_name} created")

    @commands.command()
    async def createpr(self, ctx, branch_name, pr_title, pr_body):
        '''
        create a pull request from existing branch to main branch.
        input: branch_name, pr_title, pr_body
        '''
        repo = self.github.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
        repo.create_pull(title=pr_title, body=pr_body, head=branch_name, base="main")
        await ctx.send(f"pull request {pr_title} created")
    
    @commands.command()
    async def editfile(self, ctx, file_path, file_content):
        '''
        edit a file in a GitHub repository.
        input: file_path, file_content
        '''
        repo = self.github.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
        file = repo.get_contents(file_path)
        repo.update_file(file.path, "update file", file_content, file.sha)
        await ctx.send(f"file {file_path} updated")

    @commands.command()
    async def createfile(self, ctx, file_path, file_content):
        '''
        create a file in a GitHub repository.
        input: file_path, file_content
        '''
        repo = self.github.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
        repo.create_file(file_path, "create file", file_content)
        await ctx.send(f"file {file_path} created")

def recursive_list_files(repo, path):
    contents = repo.get_contents(path)
    # print(contents)
    files = []

    for content in contents:
        if content.type == "dir":
            files.extend(recursive_list_files(repo, content.path))
        elif content.type == "file":
            files.append(content.path)

    return files
async def setup(bot):
    await bot.add_cog(GithubCog(bot))
