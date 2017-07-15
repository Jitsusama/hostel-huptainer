#!/usr/bin/env groovy

node {
    stage("Environment Setup") {
        echo "Grab Code"
        checkout scm

        echo "Remove Old Run Data"
        sh "rm -r *test-results.xml *coverage.xml build dist *.egg-info || exit 0"

        echo "Create Python 2.7 Build Environment"
        python_build = docker.build("python:2.7-hostel-env", "-f tests/envs/python2.7/Dockerfile .")
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

    stage("Run Test Suite") {
        parallel py27: {
            echo "Create Python 2.7 Environment"
            python_27 = docker.build("python:2.7-hostel-env", "-f tests/envs/python2.7/Dockerfile .")

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
            python_36 = docker.build("python:3.6-hostel-env", "-f tests/envs/python3.6/Dockerfile .")

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
        }, certbot: {
            echo "Create hostel-huptainer Environment"
            spinner = docker.image("python:2.7").run(
                "--label 'org.eff.certbot.cert_cns=hostel-huptainer.grrbrr.ca'",
                "python2 -c 'import signal\ndef h(*args): raise Exception(\"HUPPED\")\nsignal.signal(signal.SIGHUP, h)\nwhile True: pass\n'")

            docker.build("hostel-huptainer", ".").inside {
                withEnv(["CERTBOT_HOSTNAME=hostel-huptainer.grrbrr.ca"]) {
                    sh "hostel-huptainer && sleep 1"
                }
            }

            try { sh "docker logs ${spinner.id} 2>&1 | grep \"Exception: HUPPED\"" }
            catch (e) {
                echo "hostel-huptainer didn't SIGHUP container: ${e}"
                currentBuild.status = "UNSTABLE"
            }

            spinner.stop()
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
