CREATE VIEW listar_escolas_por_qt_alunos AS
SELECT escola.CO_ENTIDADE, escola.NO_ENTIDADE, COUNT(matricula.ID_MATRICULA) AS contagem_estudantes
FROM escola
LEFT JOIN matricula ON escola.CO_ENTIDADE = matricula.CO_ENTIDADE
GROUP BY escola.CO_ENTIDADE, escola.NO_ENTIDADE
ORDER BY contagem_estudantes DESC;