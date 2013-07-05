#version 330 core
layout(location = 0) in vec4 vertexPosition_modelspace;
layout(location = 1) in vec3 vertexColor;
out vec3 fragmentColor;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform mat4 translate;

void main()
{
    gl_Position = (projectionMatrix * viewMatrix * modelMatrix) * vertexPosition_modelspace;

    fragmentColor = vertexColor;
}