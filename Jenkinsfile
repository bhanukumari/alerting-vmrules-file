pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/bhanukumari/alerting-vmrules-file.git'
            }
        }

        stage('Install Python') {
            steps {
                sh '''
                    if [ ! -f /tmp/python/bin/python3 ]; then
                        curl -L https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.11.7+20240107-x86_64-unknown-linux-gnu-install_only.tar.gz -o /tmp/python.tar.gz
                        tar -xzf /tmp/python.tar.gz -C /tmp/
                    fi
                    /tmp/python/bin/pip3 install pyyaml
                '''
            }
        }

        stage('Convert YAML to JSON') {
            steps {
                sh '/tmp/python/bin/python3 convert.py'
            }
        }

        // stage('Generate Postman Collection') {
        //     steps {
        //         sh '/tmp/python/bin/python3 generate_postman.py'
        //     }
        // }
    }
}









