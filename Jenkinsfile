pipeline {
agent any

```
triggers {
    githubPush()
}

stages {
    stage('Clone Repo') {
        steps {
            git branch: 'main',
                url: 'https://github.com/bhanukumari/alerting-vmrules-file.git'
        }
    }

    stage('Check Python') {
        steps {
            sh '''
            python3 --version
            pip3 --version
            '''
        }
    }

    stage('Install Dependencies') {
        steps {
            sh '''
            pip3 install pyyaml --user
            '''
        }
    }

    stage('Convert YAML to JSON') {
        steps {
            sh '''
            python3 convert.py
            '''
        }
    }

    stage('Verify Output') {
        steps {
            sh '''
            ls -la json_output
            '''
        }
    }
}
```

}

