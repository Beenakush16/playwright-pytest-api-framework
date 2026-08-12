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

        gitParameter(
            name: 'BRANCH',
            type: 'PT_BRANCH',
            defaultValue: 'main',
            branchFilter: 'origin/(.*)',
            sortMode: 'DESCENDING_SMART',
            selectedValue: 'DEFAULT',
            quickFilterEnabled: true,
            description: 'Select Git branch'
        )

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

        PYTHON = "/opt/homebrew/bin/python3.13"

        VENV = "venv"

        ALLURE_RESULTS = "allure-results"

    }

    stages {

        stage('Checkout Source') {

            steps {
                checkout([
                    $class: 'GitSCM',

                    branches: [[
                        name: "*/${params.BRANCH}"
                    ]],

                    userRemoteConfigs: [[
                        url: 'https://github.com/Beenakush16/playwright-pytest-api-framework.git'
                    ]]
                ])
        }

        }

        stage('Verify Build Environment') {

            steps {

                sh '''
                    echo "===== Workspace ====="

                    pwd

                    echo ""

                    echo "===== Repository ====="

                    ls -la

                    echo ""

                    echo "===== Python ====="

                    ${PYTHON} --version

                    ${PYTHON} -c "import sys; print(sys.executable)"

                    echo ""

                    echo "===== Git ====="

                    git --version
                '''

            }

        }

        stage('Create Virtual Environment') {

            steps {

                sh '''
                    rm -rf ${VENV}

                    ${PYTHON} -m venv ${VENV}

                    ${VENV}/bin/python --version

                    ${VENV}/bin/python -c "import sys; print(sys.executable)"

                    ${VENV}/bin/python -c "import sys; print(sys.version)"
                '''

            }

        }

        stage('Install Dependencies') {

            steps {

                sh '''

                    ${VENV}/bin/python -m pip install --upgrade pip

                    ${VENV}/bin/python -m pip install -r requirements.txt
                '''

            }

        }

        stage('Start Mock Server') {

            steps {

                sh '''
                    nohup python mock_server/app.py > mock_server.log 2>&1 &

                    sleep 5
                '''

            }

        }

        stage('Run API Tests') {

            steps {

                sh """
                    ${VENV}/bin/pytest \
                        tests/ \
                        --env=${params.ENV} \
                        --alluredir=${ALLURE_RESULTS} \
                        --junitxml=test-results/junit.xml
                """

            }

        }
        stage('Verify Allure Results') {

            steps {

                sh '''
                    echo "===== Workspace ====="

                    pwd

                    echo ""

                    echo "===== Allure Results ====="

                    ls -la allure-results

                     echo ""

                    echo "===== executor.json ====="

                    cat allure-results/executor.json || true
                '''

            }

        }
        stage('Debug Allure') {
            steps {
                sh '''
                    echo "===== Current Workspace ====="
                    pwd

                    echo ""

                    echo "===== allure-results ====="
                    ls -la allure-results

                    echo ""

                    echo "===== executor.json ====="
                    cat allure-results/executor.json
                    '''
            }
        }

    }

    post {

        always {

            allure(
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']],
                commandline: 'Allure'
            )

            junit(
                testResults: 'test-results/junit.xml',
                allowEmptyResults: true,
                keepLongStdio: true
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