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
Imagen después. Se corrió varias veces pylint, y se llegó al resultado después de agregar docstrings.
Algunos unused imports son para dar contexto a esa parte del código.
![image](https://github.com/SVA-BL00/RamenAI/assets/157633346/6039b8a6-82cc-4b47-8248-ea0ccf7db778)
Ahora tenemos de puntuación un 8.70, a comparación del 6.97 del inicio.

### Ejemplo de format
Para mantener un estandar en el trabajo, se utilizó la librería de black.
![image](https://github.com/SVA-BL00/RamenAI/assets/157633346/62e1c842-8190-4308-b6f7-6a45667f1445)

**Para ver cómo se modificó el código más a detalle, entrar a la rama "tools".**
