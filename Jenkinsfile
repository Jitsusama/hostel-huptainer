#!/usr/bin/env groovy

node {
    stage("Environment Setup") {
        echo "Grab Code"
        checkout scm

        echo "Remove Old Run Data"
        sh "rm -r *test-results.xml *coverage.xml build dist *.egg-info || exit 0"

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

                try {
                    echo "Run py.test Test Suite"
                    sh "py.test --cache-clear --pylama --junit-xml py27-test-results.xml --junit-prefix py27"
                }
                catch (e) {}
                junit "py27-test-results.xml"
            }
            python_27.inside {
                echo "Install in Editable Mode"
                sh "pip install -e ."
                try {
                    echo "Obtain Code Coverage for Unit Tests"
                    sh "coverage run -p --source source/hostel_huptainer -m pytest tests/unit"
                }
                catch (e) {}
            }
        }, py36: {
            echo "Create Python 3.6 Environment"
            python_36 = docker.build("python:3.6-hostel-env", "-f ci-cd/py36-env/Dockerfile .")

            python_36.inside {
                echo "Install Wheel Artifact"
                sh "pip install dist/*.whl"

                xmlFile = "py36-test-results.xml"
                try {
                    echo "Run py.test Test Suite"
                    sh "py.test --cache-clear --pylama --junit-xml py36-test-results.xml --junit-prefix py36"
                }
                catch (e) {}
                junit "py36-test-results.xml"
            }
            python_36.inside {
                echo "Install in Editable Mode"
                sh "pip install -e ."
                try {
                    echo "Obtain Code Coverage for Unit Tests"
                    sh "coverage run -p --source source/hostel_huptainer -m pytest tests/unit"
                }
                catch (e) {}
            }
        }
        echo "Check Code Coverage"
        python_build.inside {
            sh "coverage combine"
            sh "coverage xml"
            step([$class: 'CoberturaPublisher', autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'coverage.xml', failUnhealthy: false, failUnstable: false, maxNumberOfBuilds: 0, onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: true])
            sh "coverage erase"
        }
    }

    stage("Archive Python Artifacts") {
        archiveArtifacts artifacts: "dist/*",
                fingerprint: true,
                onlyIfSuccessful: true
    }
}
