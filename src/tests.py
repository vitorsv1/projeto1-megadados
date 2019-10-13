from biblioteca import *

class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='red_soc_passaros'
        )
    
    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
    
    def setUp(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION')

    def tearDown(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('ROLLBACK')

    def test_adiciona_usuario(self):
        conn = self.__class__.connection
        
        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Cria"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"

        adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)

        try:
            adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)
            self.fail('Não deveria ter adicionado o mesmo usuario duas vezes')
        except ValueError as e:
            pass
        
        id = acha_usuario(conn, nick)
        self.assertIsNotNone(id)

        id = acha_usuario(conn, 'pokadskopdsa')
        self.assertIsNone(id)

    def test_acha_usuario(self):
        conn = self.__class__.connection
        id=10
        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Cria"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn,nick, nome, sobrenome, email, cidade)

        id=acha_usuario(conn,"Jukes")
        self.assertIsNotNone(id)

    def test_desativa_usuario(self):
        conn = self.__class__.connection

        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Desativa"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)
        id = acha_usuario(conn, nick)

        res = lista_usuario(conn)
        self.assertCountEqual(res, (id,))

        desativa_usuario(conn, id)

        res = esta_desativado_usuario(conn, id)
        self.assertFalse(res)

    def test_muda_nick_usuario(self):
        conn = self.__class__.connection

        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Cria"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"

        adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)
        adiciona_usuario(conn, "Jukera", nome, sobrenome, email, cidade)
        id = acha_usuario(conn,"Jukera")

        try:
            muda_nick_usuario(conn, id, "Jukes")
            self.fail('Não deveria ter mudado o nome.')
        except ValueError as e:
            pass

        muda_nick_usuario(conn, id, 'MecLord')

        id_novo = acha_usuario(conn,'MecLord')
        self.assertEqual(id,id_novo)

    def test_lista_usuarios(self):
        conn = self.__class__.connection
        res=lista_usuario(conn)
        self.assertFalse(res)
        
        usuariosids=[]
        for i in range(3):
            nick="JuninhoXD{}".format(i)
            adiciona_usuario(conn,nick,"Junior","Teste","teste@teste.com","testelandia")
            usuariosids.append(acha_usuario(conn,nick))
        
        res=lista_usuario(conn)
        self.assertCountEqual(res,usuariosids)

        for j in usuariosids:
            desativa_usuario(conn,j)
        
        for k in usuariosids:
            res=esta_desativado_usuario(conn, k)
            self.assertFalse(res)
    
    def test_visualiza_post(self):
        conn = self.__class__.connection

        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Visualiza"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn,nick, nome, sobrenome, email, cidade)
        id = acha_usuario(conn,nick)

        titulo= "Teste post"
        texto = "aoskdoapsdk"
        url = "sokdapodkpao.com"
        adiciona_post(conn, id,titulo,texto, url)
        id_post = acha_post(conn, titulo)

        visualiza_post(conn, id_post, id, "Android", "192.129.3.1","Chrome", "2019-02-01")

        try:
            visualiza_post(conn, id_post, id, "Android", "192.129.3.1","Chrome", "2019-02-01")
            self.fail("Não deveria adicionar uma visualizacao nova")
        except ValueError as e:
            pass

    def test_lista_visualizadores_post(self):
        conn = self.__class__.connection
        
        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Lista Visualiza"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn,nick, nome, sobrenome, email, cidade)
        id = acha_usuario(conn,nick)

        titulo= "Teste post2"
        texto = "aoskdoapsdk"
        url = "sokdapodkpao.com"
        adiciona_post(conn, id,titulo,texto, url)
        id_post = acha_post(conn, titulo)

        visualiza_post(conn, id_post, id, "Android", "192.129.3.1","Chrome", "2019-02-01")

        res=lista_visualizadores_post(conn, id_post)
        self.assertTrue(res)
        
        usuariosids=[id]
        for i in range(3):
            nick="JuninhoXD{}".format(i)
            adiciona_usuario(conn,nick,"Junior","Teste","teste@teste.com","testelandia")
            id = acha_usuario(conn,nick)
            visualiza_post(conn, id_post, id, "Android", "192.129.3.1","Chrome", "2019-02-01")
            usuariosids.append(id)

        res=lista_visualizadores_post(conn, id_post)
        self.assertCountEqual(res,usuariosids)
     
    def test_lista_posts_visualizados_usuario(self):
        conn = self.__class__.connection

        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Lista Visualiza"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn,nick, nome, sobrenome, email, cidade)
        id = acha_usuario(conn,nick)

        titulo= "Teste post2"
        texto = "aoskdoapsdk"
        url = "sokdapodkpao.com"

        postsids=[]
        for i in range(3):
            titulo="TituloTest{}".format(i)
            adiciona_post(conn, id,titulo,texto, url)
            id_post = acha_post(conn, titulo)
            visualiza_post(conn, id_post, id, "Android", "192.129.3.1","Chrome", "2019-02-01")
            postsids.append(id_post)

        res=lista_posts_visualizados_usuario(conn,id)
        self.assertCountEqual(res,postsids)

def run_sql_script(filename):
    global config
    with open(filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'], 
                '-u', config['USER'], 
                '-p' + config['PASS'], 
                '-h', config['HOST']
            ], 
            stdin=f
        )

def setUpModule():
    filenames = [entry for entry in os.listdir() 
        if os.path.isfile(entry) and re.match(r'.*_\d{3}\.sql', entry)]
    for filename in filenames:
        run_sql_script(filename)

def tearDownModule():
    run_sql_script('script_criacao.sql')

if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)
