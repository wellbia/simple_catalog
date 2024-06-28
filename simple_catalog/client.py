import os
import socket

from datetime import datetime

from .database import Database
from .hash import get_sha256_hash, get_file_hash


class Client(Database):
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
        salt: str,
        product: str = None,
        revision: str = None,
        hash: str = None,
        verbose: bool = False,
    ):
        super().__init__(host, user, password, database)
        self.salt = salt
        self.product = product
        self.revision = revision
        self.hash = hash
        self.build_machine = socket.gethostname()
        self.BATCH_SIZE = 512
        self.verbose = verbose

    def add_files(self, files):
        if not self.table_exists():
            self.create_table()

        batches = [
            files[i : i + self.BATCH_SIZE]
            for i in range(0, len(files), self.BATCH_SIZE)
        ]

        for batch in batches:
            self.__add_files_batch(batch)

    def __add_files_batch(self, batch):
        values = []
        placeholders = []
        for file in batch:
            md5, sha256, entry = get_file_hash(
                file, self.product, self.revision, self.hash, self.salt
            )

            if self.verbose:
                print(f"add {file} => {md5}, {sha256}")

            values.extend(
                [
                    self.product,
                    self.build_machine,
                    self.revision,
                    os.path.basename(file),
                    self.hash,
                    md5,
                    sha256,
                    entry,
                    datetime.now(),
                ]
            )
            placeholders.append("(%s, %s, %s, %s, %s, %s, %s, %s, %s)")

        query = f"""
        INSERT INTO catalog(
            product, build_machine, revision, filename, 
            repository_hash, md5_hash, sha256_hash, entry_hash, update_time
        ) VALUES {', '.join(placeholders)}
        """

        self.execute(query, values)

    def add(self, file: str):
        if not self.table_exists():
            self.create_table()

        md5, sha256, entry = get_file_hash(
            file, self.product, self.revision, self.hash, self.salt
        )

        if self.verbose:
            print(f"add {file} => {md5}, {sha256}")

        query = """
        INSERT INTO catalog(
            product, build_machine, revision, filename,
            repository_hash, md5_hash, sha256_hash, entry_hash, update_time
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.execute(
            query,
            (
                self.product,
                self.build_machine,
                self.revision,
                os.path.basename(file),
                self.hash,
                md5,
                sha256,
                entry,
                datetime.now(),
            ),
        )

    def delete(self, file: str) -> tuple:
        if not self.table_exists():
            return None

        md5, sha256, entry = get_file_hash(
            file, self.product, self.revision, self.hash, self.salt
        )
        query = "SELECT * FROM catalog WHERE md5_hash=%s and sha256_hash=%s and entry_hash=%s and product=%s and revision=%s"
        args = (md5, sha256, entry, self.product, self.revision)
        removed = self.select_all(query, args)

        query = "DELETE FROM catalog WHERE md5_hash=%s and sha256_hash=%s and entry_hash=%s and product=%s and revision=%s"
        self.execute(query, args)

        return removed

    def check(self, file: str) -> tuple:
        sha256 = get_sha256_hash(file)
        query = "SELECT * FROM catalog WHERE sha256_hash=%s"
        return self.select_all(query, (sha256,))

    def table_exists(self) -> bool:
        query = "SELECT * FROM information_schema.tables WHERE table_name=%s"
        if self.select_one(query, ("catalog",)) is not None:
            return True
        return False

    def create_table(self):
        query = """
            CREATE TABLE catalog (
                id int(11) NOT NULL AUTO_INCREMENT,
                product varchar(255) NOT NULL,
                build_machine varchar(255) NOT NULL,
                revision varchar(255) NOT NULL,
                filename varchar(255) NOT NULL,
                repository_hash varchar(255) NOT NULL,
                md5_hash varchar(255) NOT NULL,
                sha256_hash varchar(255) NOT NULL,
                entry_hash varchar(255) NOT NULL,
                update_time datetime NOT NULL,
                PRIMARY KEY (id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        self.execute(query)
