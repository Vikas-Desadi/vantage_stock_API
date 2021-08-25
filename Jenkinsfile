pipeline {
    agent any

    stages {
        stage('checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github_pass', url: 'https://github.com/Vikas-Desadi/vantage_stock_API.git']]])
            }
        }
        stage('Test') {
            steps {
                echo "pytest -v -s"
                sh 'pytest -v -s --junit-xml test-reports/results.xml'
            }
            post{
                always{
                    junit 'test-reports/results.xml'
                }
            }
        }

        stage('Slack') {
            steps{
                slackSend channel: '#python', teamDomain: 'testing-github-slack', tokenCredentialId: 'b5d565ab-f579-4202-88c9-ba7e5c394552'
            }
        }

    }
}
