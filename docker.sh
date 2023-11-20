# Build & push docker image
# Arguments: 
#   --build - build docker image
#   --push - push to gitlab repo
#   -f <dockerfilename> - Use a custom dockerfile


while [[ $# -gt 0 ]]; do
  case $1 in
    --build)
      DO_BUILD="T"
      shift # past argument
      ;;
    --push)
      DO_PUSH="T"
      shift # past argument
      ;;
    -f)
      DOCKERFILE="$2"
      shift 2 # past argument
      ;;
    -variation)
      VARIATION="-$2"
      DOCKERFILE="Dockerfile${VARIATION}"
      shift 2 # past argument
      ;;
  esac
done

EL_IMAGE_NAMESPACE=ecoloop-platform/
EL_IMAGE_NAME=ecoloop-ml${VARIATION}
# GitLab
# DOCKER_REGISTRY=registry.gitlab.com
# REGISTRY_NAMESPACE=${DOCKER_REGISTRY}/hanaloop/sustainability/ecoloop-platform
# DockerHub
REGISTRY_NAMESPACE=hanalooper/


# Dockerfile-arm
if [ -z "$DOCKERFILE" ]; then
  DOCKERFILE="Dockerfile"
fi

if [ -z "${EL_IMAGE_TAG}" ]; then
  EL_IMAGE_TAG=0.8.7
  echo "EL_IMAGE_TAG setting to default ${EL_IMAGE_TAG}"
fi

EL_IMAGE_FULL_NAME=${EL_IMAGE_NAMESPACE}${EL_IMAGE_NAME}

if [ "$DO_BUILD" = "T" ]; then
  echo "Building ${EL_IMAGE_FULL_NAME}"

  # docker build -t hanaloop/ecoloop-ml:0.1 -f .
  docker build -t ${EL_IMAGE_FULL_NAME}:${EL_IMAGE_TAG} . -f ${DOCKERFILE}
  docker tag ${EL_IMAGE_FULL_NAME}:${EL_IMAGE_TAG} ${EL_IMAGE_FULL_NAME}:latest
fi

if [ "$DO_PUSH" = "T" ]; then
  # You will need to login to container first
  REMOTE_IMAGE_FULL_NAME=${REGISTRY_NAMESPACE}${EL_IMAGE_NAME}
  # docker login ${DOCKER_REGISTRY} -u ${CONGTAINER_REGISTRY_USER} -p ${CONTAINER_REGISTRY_TOKEN}

  echo "Tagging & pushing ${EL_IMAGE_FULL_NAME} as ${REMOTE_IMAGE_FULL_NAME} with latest and ${EL_IMAGE_TAG} tags"
  docker tag ${EL_IMAGE_FULL_NAME} ${REMOTE_IMAGE_FULL_NAME}:latest
  docker tag ${EL_IMAGE_FULL_NAME} ${REMOTE_IMAGE_FULL_NAME}:${EL_IMAGE_TAG}

  # push to registry
  docker push ${REMOTE_IMAGE_FULL_NAME}:latest
  docker push ${REMOTE_IMAGE_FULL_NAME}:${EL_IMAGE_TAG}
fi
