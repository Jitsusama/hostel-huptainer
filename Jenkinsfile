#!/usr/bin/env groovy

node {
    stage("Environment Setup") {
        echo "Grab Code"
        checkout scm

        echo "Remove Old Run Data"
        sh "rm -r *test-results.xml || exit 0"

        echo "Create Python 2.7 Build Environment"
        python_build = docker.build("python:2.7-hostel-env", "-f ci-cd/py27-env/Dockerfile .")
    }

    stage("Build Python Artifacts") {
        python_build.inside {
            echo "Remove Old Artifacts"
            sh "rm dist/* || exit 0"

            echo "Create Source Artifact"
            sh "python setup.py sdist"

            echo "Create Wheel Artifact"
            sh "python setup.py bdist_wheel"
        }
    }

    stage("Run Python Test Suite") {
        parallel py27: {
            echo "Create Python 2.7 Environment"
            python_27 = docker.build("python:2.7-hostel-env", "-f ci-cd/py27-env/Dockerfile .")

            python_27.inside {
                echo "Install Wheel Artifact"
                sh "pip install dist/*.whl"

                echo "Run py.test Test Suite"
                try {
                    sh "py.test --pylama --junit-xml py27-test-results.xml --junit-prefix py27"
                }
                finally {
                    junit "py27-test-results.xml"
                }
            }
        }, py36: {
            echo "Create Python 3.6 Environment"
            python_36 = docker.build("python:3.6-hostel-env", "-f ci-cd/py36-env/Dockerfile .")

            python_36.inside {
                echo "Install Wheel Artifact"
                sh "pip install dist/*.whl"

                echo "Run py.test Test Suite"
                xmlFile = "py36-test-results.xml"
                try {
                    sh "py.test --pylama --junit-xml py36-test-results.xml --junit-prefix py36"
                }
                finally {
                    junit "py36-test-results.xml"
                }
            }
        }
    }

    stage("Archive Python Artifacts") {
        archiveArtifacts artifacts: "dist/*",
                fingerprint: true,
                onlyIfSuccessful: true
    }
}