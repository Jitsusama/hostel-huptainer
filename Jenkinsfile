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
            spinnerImage = docker.image("python:2.7")
            spinnerContainer = spinner.run(
                    "--label 'org.eff.certbot.cert_cns=test.grrbrr.ca'",
                    'python2 -c "import signal;def h(*args): raise Exception();signal.signal(signal.SIGHUP, h);while True: pass"')
            certbot = docker.build("hostel-huptainer", ".")

            certbot.inside {
                withCredentials([string(credentialsId: 'DO_APIKEY', variable: 'DO_APIKEY'),
                                 string(credentialsId: 'DO_DOMAIN', variable: 'DO_DOMAIN'),
                                 string(credentialsId: 'CERTBOT_EMAIL', variable: 'CERTBOT_EMAIL')]) {
                    withEnv(["DO_APIKEY = $DO_APIKEY", "DO_DOMAIN = $DO_DOMAIN"], "LETS_DO_POSTCMD = hostel-huptainer") {
                        sh """\
certbot certonly --manual\
    --manual-auth-hook lets-do-dns --manual-cleanup-hook lets-do-dns\
    --preferred-challenges dns -d test.$DO_DOMAIN --test-cert --manual-public-ip-logging-ok\
    --non-interactive --agree-tos --email $CERTBOT_EMAIL"""
                    }
                }
            }
            sleep(1000 as long)
            spinnerContainer.stop()
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
