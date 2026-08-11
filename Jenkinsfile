pipeline {

    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(
            logRotator(
                numToKeepStr: '20'
            )
        )
    }

    parameters {

        choice(
            name: 'ENV',
            choices: [
                'qa',
                'uat',
                'prod'
            ],
            description: 'Select execution environment'
        )

    }

    environment {

        PYTHON = "python3"

        VENV = "venv"

        ALLURE_RESULTS = "allure-results"

    }

    stages {

        stage('Checkout Source') {

            steps {
                checkout scm
            }

        }

        stage('Verify Build Environment') {

            steps {

                sh '''
                    echo "Workspace:"

                    pwd

                    echo ""

                    echo "Repository Files:"

                    ls -la

                    echo ""

                    python3 --version

                    pip3 --version

                    git --version
                '''

            }

        }

        stage('Create Virtual Environment') {

            steps {

                sh '''
                    ${PYTHON} -m venv ${VENV}
                '''

            }

        }

        stage('Install Dependencies') {

            steps {

                sh '''
                    . ${VENV}/bin/activate

                    python -m pip install --upgrade pip

                    pip install -r requirements.txt
                '''

            }

        }

        stage('Start Mock Server') {

            steps {

                sh '''
                    . ${VENV}/bin/activate

                    nohup python mock_server/app.py > mock_server.log 2>&1 &

                    sleep 5
                '''

            }

        }

        stage('Run API Tests') {

            steps {

                sh """
                    . ${VENV}/bin/activate

                    pytest tests/ \
                        --env=${params.ENV} \
                        --alluredir=${ALLURE_RESULTS}
                """

            }

        }

    }

    post {

        always {

            allure(
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            )

            archiveArtifacts(
                artifacts: 'logs/**/*',
                allowEmptyArchive: true
            )

            archiveArtifacts(
                artifacts: 'mock_server.log',
                allowEmptyArchive: true
            )

            sh '''
                pkill -f "mock_server/app.py" || true
            '''
        }

        success {

            echo "API Automation execution completed successfully."

        }

        failure {

            echo "API Automation execution failed."

        }

    }

}