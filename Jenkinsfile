// Xenohuru API — Jenkins pipeline
//
// Builds the same Docker image that ships to production, tests it against
// a real Postgres via docker compose, then (on main) deploys it over SSH.
// Pushing a "v*" tag builds and labels a release image instead of deploying.
//
// Required Jenkins credentials:
//   xenohuru-do-ssh-key   SSH private key for the deploy user
//   xenohuru-do-host      Secret text, the production host
//   xenohuru-do-user      Secret text, the SSH user
//
// Triggering on push:
//   This job only *reacts* to pushes — it doesn't get notified unless a
//   webhook tells it to. To make that live:
//     1. Create this job as a "Multibranch Pipeline" (or GitHub Organization)
//        job using the GitHub Branch Source plugin, pointed at this repo.
//     2. In GitHub: Settings -> Webhooks -> Add webhook
//          Payload URL:  https://<your-jenkins-host>/github-webhook/
//          Content type: application/json
//          Events:       "Just the push event" (add "tag push" too if using
//                         a plain Pipeline job instead of multibranch)
//     3. In Jenkins job config, enable "GitHub hook trigger for GITScm polling".
//   Until a Jenkins host is reachable from the internet (or from GitHub's
//   webhook IPs), builds have to be triggered manually or by SCM polling —
//   the githubPush() trigger below is a no-op until the webhook exists.

pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    triggers {
        githubPush()
    }

    environment {
        COMPOSE_PROJECT_NAME = "xenohuru-ci-${BUILD_NUMBER}"
        SECRET_KEY            = 'ci-secret-key-not-for-production'
        DEBUG                 = 'True'
        ALLOWED_HOSTS         = 'localhost,127.0.0.1'
        DB_NAME               = 'xenohuru_test'
        DB_USER               = 'postgres'
        DB_PASSWORD           = 'postgres'
        FRONTEND_URL          = 'http://localhost:8000'
        EMAIL_BACKEND         = 'django.core.mail.backends.console.EmailBackend'
    }

    stages {
        stage('Prepare') {
            steps {
                // docker-compose.yml reads env_file: .env — CI supplies its
                // config via the environment{} block above and -e flags, so
                // this just needs to exist for compose to parse the file.
                sh 'touch .env'
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    python3 -m venv .venv-lint
                    . .venv-lint/bin/activate
                    pip install --quiet ruff==0.14.0
                    ruff check .
                '''
            }
        }

        stage('Build image') {
            steps {
                sh 'docker compose build web'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker compose up -d db
                    docker compose run --name xenohuru-test-${BUILD_NUMBER} \
                        -e SECRET_KEY -e DEBUG -e ALLOWED_HOSTS \
                        -e DB_NAME -e DB_USER -e DB_PASSWORD \
                        -e FRONTEND_URL -e EMAIL_BACKEND \
                        --entrypoint '' \
                        web sh -c "
                            python manage.py makemigrations --check --dry-run &&
                            python manage.py migrate --no-input &&
                            python manage.py check &&
                            coverage run manage.py test --verbosity=2 &&
                            coverage report &&
                            coverage xml
                        "; TEST_EXIT=$?
                    docker cp xenohuru-test-${BUILD_NUMBER}:/app/coverage.xml coverage.xml || true
                    docker rm -f xenohuru-test-${BUILD_NUMBER} || true
                    exit $TEST_EXIT
                '''
            }
        }

        stage('Tag release image') {
            when {
                tag pattern: 'v\\d+\\.\\d+\\.\\d+', comparator: 'REGEXP'
            }
            steps {
                sh '''
                    docker tag ${COMPOSE_PROJECT_NAME}-web:latest xenohuru-web:${TAG_NAME}
                    echo "Built release image xenohuru-web:${TAG_NAME}"
                    echo "Push it to your registry here once one is configured, e.g.:"
                    echo "  docker tag xenohuru-web:${TAG_NAME} <registry>/xenohuru-web:${TAG_NAME}"
                    echo "  docker push <registry>/xenohuru-web:${TAG_NAME}"
                '''
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([
                    string(credentialsId: 'xenohuru-do-host', variable: 'DO_HOST'),
                    string(credentialsId: 'xenohuru-do-user', variable: 'DO_USER')
                ]) {
                    sshagent(credentials: ['xenohuru-do-ssh-key']) {
                        sh '''
                            ssh -o StrictHostKeyChecking=no ${DO_USER}@${DO_HOST} '
                                set -e
                                cd /var/www/xenohuru-api
                                git fetch origin main
                                git clean -fd
                                git reset --hard origin/main
                                docker compose up -d --build
                            '
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker compose down -v --remove-orphans || true'
            archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
        }
    }
}
