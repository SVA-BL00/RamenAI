## Unit tests, lint y format
RamenAI usa pytest para realizar pruebas de unidad, pylint para pruebas estáticas y black para el formateo.
### Ejemplo de pytest
![image](https://github.com/SVA-BL00/RamenAI/assets/157633346/1f793186-db2d-461d-8e54-653f4887e410)
Para ver el coverage y las líneas faltantes:
![image](https://github.com/SVA-BL00/RamenAI/assets/157633346/cf6a4015-235d-4759-a3e0-32a88585027d)
_El archivo conftest no está al 100%, pero solo se utiliza para configurar las pruebas como tal. En cuanto a views, las líneas faltantes corresponden a los requests de OpenAI, que por la complejidad de implementar, están fuera del alcance de este proyecto._

### Ejemplo de pylint
Imagen antes
![image](https://github.com/SVA-BL00/RamenAI/assets/157633346/001765a1-2a42-4a67-9e34-cbee4f2a5cfd)
