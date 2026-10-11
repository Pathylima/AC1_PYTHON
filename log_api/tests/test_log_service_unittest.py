
import tempfile
import unittest
from pathlib import Path

from log_service import write_log, read_logs


class TestLogService(unittest.TestCase):

    def setUp(self):
        # Cria uma pasta temporária para cada teste
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = Path(self.temp_dir.name) / "app.log"

    def tearDown(self):
        # Remove a pasta temporária após cada teste
        self.temp_dir.cleanup()

    def test_cria_arquivo_ao_gravar(self):
        write_log("[INFO] Teste", self.log_path)

        self.assertTrue(self.log_path.exists())

    def test_acrescenta_registros_em_ordem(self):
        write_log("[INFO] Primeiro", self.log_path)
        write_log("[WARNING] Segundo", self.log_path)

        self.assertEqual(
            read_logs(self.log_path),
            ["[INFO] Primeiro", "[WARNING] Segundo"]
        )

    def test_permite_mensagens_duplicadas(self):
        write_log("[INFO] Repetido", self.log_path)
        write_log("[INFO] Repetido", self.log_path)

        self.assertEqual(
            read_logs(self.log_path),
            ["[INFO] Repetido", "[INFO] Repetido"]
        )

    def test_le_arquivo_inexistente(self):
        self.assertEqual(read_logs(self.log_path), [])

    def test_le_arquivo_vazio(self):
        self.log_path.touch()

        self.assertEqual(read_logs(self.log_path), [])

    def test_preserva_caracteres_especiais(self):
        mensagem = '[INFO] Ação concluída, "tudo certo".'
        write_log(mensagem, self.log_path)

        self.assertEqual(read_logs(self.log_path), [mensagem])

    def test_preserva_registros_apos_reabrir_arquivo(self):
        write_log("[INFO] Registro persistente", self.log_path)

        # A leitura abre o arquivo novamente
        registros = read_logs(self.log_path)

        self.assertEqual(registros, ["[INFO] Registro persistente"])

    def test_destino_invalido_gera_erro(self):
        caminho_invalido = Path(self.temp_dir.name) / "inexistente" / "app.log"

        with self.assertRaises(OSError):
            write_log("[INFO] Teste", caminho_invalido)


if __name__ == "__main__":
    unittest.main()
